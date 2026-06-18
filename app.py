"""
Graphify Core — Backend FastAPI v2.0
=====================================
Plataforma unificada: Grafo interactivo + Monitoreo SSE + Chatbot Gemini Graph-RAG.

Endpoints:
  GET  /                → Sirve index.html (frontend)
  GET  /graph-view      → Sirve graphify-out/graph.html (grafo real interactivo)
  GET  /api/activity    → Historial de actividades reales
  GET  /api/stream      → SSE: broadcast en tiempo real desde webhook
  POST /api/webhook/git → Webhook: inyecta actividad real y propaga vía SSE
  POST /api/chat        → Chatbot Graph-RAG con Gemini API + graph.json
  GET  /api/health      → Health check
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

# ═══════════════════════════════════════════════════
#  CONFIGURACIÓN — API KEY DE GEMINI
#  ═══════════════════════════════════════════════════
#  INYECTA TU API KEY AQUÍ o configúrala como variable
#  de entorno:  set GEMINI_API_KEY=tu_clave_aqui
#
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")   # ← API KEY AQUÍ
GEMINI_MODEL   = "gemini-1.5-flash"
# ═══════════════════════════════════════════════════

BASE_DIR        = Path(__file__).resolve().parent
GRAPH_JSON_PATH = BASE_DIR / "graphify-out" / "graph.json"
GRAPH_HTML_PATH = BASE_DIR / "graphify-out" / "graph.html"
FRONTEND_PATH   = BASE_DIR / "index.html"

app = FastAPI(title="Graphify Core", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# Modelos Pydantic
# ──────────────────────────────────────────────


class WebhookPayload(BaseModel):
    developer: str    = Field(..., min_length=1)
    project: str      = Field(..., min_length=1)
    activity: str     = Field(..., min_length=1)
    impact: str       = Field(..., pattern=r"^(Bajo|Medio|Alto)$")
    project_color: str | None = None


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1)


class ActivityItem(BaseModel):
    id: str
    developer: str
    developer_avatar: str
    project: str
    project_color: str
    activity: str
    timestamp: str
    impact: str


# ──────────────────────────────────────────────
# Almacén en memoria + Broadcast SSE
# ──────────────────────────────────────────────

activity_log: list[ActivityItem] = []
MAX_LOG = 200

sse_clients: list[asyncio.Queue] = []


def _broadcast(event_dict: dict) -> None:
    """Envía un evento a todos los clientes SSE conectados."""
    data = json.dumps(event_dict)
    dead: list[asyncio.Queue] = []
    for q in sse_clients:
        if q.full():
            dead.append(q)
        else:
            q.put_nowait(data)
    for q in dead:
        if q in sse_clients:
            sse_clients.remove(q)


# ──────────────────────────────────────────────
# Utilidades
# ──────────────────────────────────────────────

_COLOR_MAP = {
    "graphify": "blue", "api": "blue", "backend": "blue",
    "frontend": "violet", "dashboard": "violet", "ui": "violet",
    "pipeline": "green", "data": "green", "etl": "green",
    "auth": "amber", "security": "amber", "login": "amber",
    "infra": "rose", "cloud": "rose", "devops": "rose", "deploy": "rose",
}
_FALLBACK = ["blue", "violet", "green", "amber", "rose"]


def _infer_color(name: str) -> str:
    low = name.lower()
    for kw, c in _COLOR_MAP.items():
        if kw in low:
            return c
    return _FALLBACK[sum(ord(c) for c in low) % len(_FALLBACK)]


def _avatar(name: str) -> str:
    parts = name.strip().split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else name[:2].upper()


def _make_item(payload: WebhookPayload) -> ActivityItem:
    return ActivityItem(
        id=str(uuid.uuid4())[:8],
        developer=payload.developer,
        developer_avatar=_avatar(payload.developer),
        project=payload.project,
        project_color=payload.project_color or _infer_color(payload.project),
        activity=payload.activity,
        timestamp=datetime.now(timezone.utc).isoformat(),
        impact=payload.impact,
    )


# ──────────────────────────────────────────────
# Graph JSON — Carga y búsqueda
# ──────────────────────────────────────────────


def load_graph() -> dict:
    if not GRAPH_JSON_PATH.exists():
        return {"nodes": [], "hyperedges": [], "links": []}
    try:
        with open(GRAPH_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"nodes": [], "hyperedges": [], "links": []}


def search_graph_context(query: str, graph: dict, top_k: int = 8) -> list[dict]:
    """
    Búsqueda por palabras clave en IDs, labels y source_files
    de nodos e hiper-aristas del grafo.
    Incluye bigramas para coincidencias más precisas.
    """
    tokens = re.findall(r"\w+", query.lower())
    words = set(tokens)
    for i in range(len(tokens) - 1):
        words.add(f"{tokens[i]} {tokens[i+1]}")

    results: list[dict] = []

    for edge in graph.get("hyperedges", []):
        text = " ".join([
            (edge.get("label") or ""),
            (edge.get("id") or ""),
            (edge.get("source_file") or ""),
            (edge.get("relation") or ""),
        ]).lower()
        score = sum(1 for w in words if w in text)
        if score > 0:
            results.append({
                "type": "hyperedge",
                "id": edge.get("id"),
                "label": edge.get("label"),
                "nodes": edge.get("nodes", []),
                "relation": edge.get("relation"),
                "confidence": edge.get("confidence"),
                "source_file": edge.get("source_file"),
                "score": score,
            })

    for node in graph.get("nodes", []):
        text = " ".join([
            (node.get("label") or ""),
            (node.get("id") or ""),
            (node.get("category") or ""),
        ]).lower()
        score = sum(1 for w in words if w in text)
        if score > 0:
            results.append({
                "type": "node",
                "id": node.get("id"),
                "label": node.get("label"),
                "category": node.get("category"),
                "score": score,
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def _format_context(context: list[dict]) -> str:
    """Formatea el contexto para inyectarlo en el prompt de Gemini."""
    if not context:
        return "Sin contexto relevante encontrado en el knowledge graph."
    lines = []
    for c in context:
        if c["type"] == "hyperedge":
            lines.append(
                f"- Hiper-arista: \"{c['label']}\" | Relación: {c.get('relation')} | "
                f"Confianza: {c.get('confidence')} | Nodos: {c.get('nodes')} | "
                f"Fuente: {c.get('source_file')}"
            )
        else:
            lines.append(f"- Nodo: \"{c['label']}\" | ID: {c['id']} | Categoría: {c.get('category')}")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# Gemini API — Integración Real
# ──────────────────────────────────────────────


async def _call_gemini(prompt: str, context: list[dict]) -> tuple[str, str]:
    """
    Llama a la API de Gemini con contexto del knowledge graph.

    Retorna: (respuesta_texto, fuente_usada)
    - Si Gemini está configurado → respuesta generativa, fuente "gemini-api"
    - Si no hay API Key → respuesta local basada en contexto, fuente "graph-local"
    """
    context_text = _format_context(context)

    # ── Sin API Key → respuesta local ──
    if not GEMINI_API_KEY:
        return _local_response(prompt, context), "graph-local"

    # ── Con API Key → llamada real a Gemini ──
    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)

        system_prompt = (
            "Eres el asistente experto de Graphify Core, una plataforma de knowledge graph. "
            "Respondes en español de forma clara, precisa y bien estructurada. "
            "Usas el contexto del grafo proporcionado para fundamentar tus respuestas. "
            "Si el contexto no es suficiente para responder, lo indicas claramente y sugieres "
            "términos de búsqueda alternativos basados en lo que sí conoces del grafo.\n\n"
            f"Contexto del knowledge graph:\n{context_text}"
        )

        response = await model.generate_content_async(
            f"{system_prompt}\n\nPregunta del usuario: {prompt}"
        )

        return response.text, "gemini-api"

    except Exception as e:
        # Si Gemini falla, caer a respuesta local con aviso
        local = _local_response(prompt, context)
        fallback = (
            f"{local}\n\n"
            f"⚠️ _Gemini no disponible ({type(e).__name__}). "
            f"Mostrando resultado local._"
        )
        return fallback, "gemini-fallback"


def _local_response(prompt: str, context: list[dict]) -> str:
    """Respuesta de respaldo basada solo en el contexto del grafo local."""
    if not context:
        return (
            f'No encontré información relevante para: **"{prompt}"**.\n\n'
            f'Prueba con: *press, espalda, hipertrofia, recuperación, rutina, '
            f'sobrecarga, pierna, hombro*.\n\n'
            f'_Configura GEMINI_API_KEY para respuestas generativas._'
        )

    lines = [f"Encontré **{len(context)}** coincidencia(s) en el knowledge graph:\n"]
    for c in context:
        if c["type"] == "hyperedge":
            lines.append(
                f"- 🔗 **{c['label']}** ({c.get('relation', 'N/A')}) "
                f"— Confianza: {c.get('confidence', 'N/A')} "
                f"| Fuente: `{c.get('source_file', 'N/A')}`"
            )
        else:
            lines.append(f"- 📌 **{c['label']}** — Categoría: {c.get('category', 'N/A')}")
    lines.append("\n_Contexto de graph.json. Con Gemini activo la respuesta será generativa._")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────


@app.get("/")
async def serve_frontend():
    if FRONTEND_PATH.exists():
        return FileResponse(FRONTEND_PATH, media_type="text/html")
    return JSONResponse({"error": "index.html no encontrado"}, status_code=404)


@app.get("/graph-view")
async def serve_graph():
    if GRAPH_HTML_PATH.exists():
        return FileResponse(GRAPH_HTML_PATH, media_type="text/html")
    return JSONResponse(
        {"error": "graphify-out/graph.html no encontrado. Ejecuta /graphify primero."},
        status_code=404,
    )


@app.get("/api/activity")
async def get_activity():
    return [item.model_dump() for item in reversed(activity_log)]


@app.post("/api/webhook/git")
async def webhook_git(payload: WebhookPayload):
    """
    Recibe datos reales y los propaga en tiempo real vía SSE.

    curl -X POST http://localhost:8000/api/webhook/git \
      -H "Content-Type: application/json" \
      -d '{"developer":"Juan Pérez","project":"Graphify API","activity":"Implementó búsqueda semántica","impact":"Alto"}'
    """
    item = _make_item(payload)
    activity_log.append(item)
    if len(activity_log) > MAX_LOG:
        activity_log.pop(0)
    _broadcast(item.model_dump())
    return {
        "status": "ok",
        "id": item.id,
        "sse_clients": len(sse_clients),
    }


@app.get("/api/stream")
async def stream_activity(request: Request):
    """SSE — Solo retransmite datos reales del webhook."""
    from sse_starlette.sse import EventSourceResponse

    queue: asyncio.Queue = asyncio.Queue(maxsize=64)
    sse_clients.append(queue)

    async def event_generator() -> AsyncGenerator:
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=15)
                    yield {"event": "activity", "data": data}
                except asyncio.TimeoutError:
                    yield {"event": "ping", "data": ""}
        finally:
            if queue in sse_clients:
                sse_clients.remove(queue)

    return EventSourceResponse(event_generator())


@app.post("/api/chat")
async def chat_endpoint(payload: ChatMessage):
    """
    Chatbot Graph-RAG.
    Lee graph.json real → busca contexto → envía a Gemini (o responde local).
    """
    graph = load_graph()
    context = search_graph_context(payload.message, graph)

    response_text, source = await _call_gemini(payload.message, context)

    return {
        "response": response_text,
        "context_count": len(context),
        "source": source,
        "graph_nodes": len(graph.get("nodes", [])),
        "graph_edges": len(graph.get("hyperedges", [])),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/health")
async def health_check():
    graph = load_graph()
    return {
        "status": "ok",
        "version": "2.0.0",
        "graph_loaded": bool(graph.get("nodes") or graph.get("hyperedges")),
        "graph_nodes": len(graph.get("nodes", [])),
        "graph_edges": len(graph.get("hyperedges", [])),
        "activity_log_size": len(activity_log),
        "sse_clients_connected": len(sse_clients),
        "gemini_configured": bool(GEMINI_API_KEY),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, log_level="info")

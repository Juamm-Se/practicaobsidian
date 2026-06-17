# Graph Report - .  (2026-06-17)

## Corpus Check
- 8 files · ~7,356 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 137 nodes · 174 edges · 12 communities (11 shown, 1 thin omitted)
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 41 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Pecho Hombro y Brazos|Pecho Hombro y Brazos]]
- [[_COMMUNITY_Espalda y Biceps|Espalda y Biceps]]
- [[_COMMUNITY_Nutricion Calorica|Nutricion Calorica]]
- [[_COMMUNITY_Pierna y Gluteos|Pierna y Gluteos]]
- [[_COMMUNITY_Programacion del Entrenamiento|Programacion del Entrenamiento]]
- [[_COMMUNITY_Metodos de Sobrecarga|Metodos de Sobrecarga]]
- [[_COMMUNITY_Gestion de Fatiga y Deload|Gestion de Fatiga y Deload]]
- [[_COMMUNITY_Pre-Entreno y Lesiones|Pre-Entreno y Lesiones]]
- [[_COMMUNITY_Recuperacion Hormonal|Recuperacion Hormonal]]
- [[_COMMUNITY_Movilidad y Recuperacion|Movilidad y Recuperacion]]
- [[_COMMUNITY_Gemelos|Gemelos]]
- [[_COMMUNITY_Braquial|Braquial]]

## God Nodes (most connected - your core abstractions)
1. `Sobrecarga Progresiva` - 12 edges
2. `Pectoral Mayor` - 11 edges
3. `Triceps` - 10 edges
4. `Biceps Braquial` - 9 edges
5. `Gluteos` - 8 edges
6. `Dorsal Ancho` - 7 edges
7. `Porcion Anterior del Deltoides` - 6 edges
8. `Press de Banca Plano` - 5 edges
9. `Romboides` - 5 edges
10. `Remo con Barra` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Aumentar el Volumen` --references--> `Volumen de Entrenamiento`  [INFERRED]
  06_sobrecarga_progresiva.md → 07_rutinas_entrenamiento.md
- `Periodizacion Lineal` --references--> `Rutina Full Body`  [INFERRED]
  06_sobrecarga_progresiva.md → 07_rutinas_entrenamiento.md
- `Sobreentrenamiento` --references--> `MRV (Maximum Recoverable Volume)`  [INFERRED]
  08_recuperacion_prevencion.md → 06_sobrecarga_progresiva.md
- `Retraccion Escapular` --prevents_injury_to--> `Manguito Rotador`  [INFERRED]
  01_ejercicios_pecho.md → 04_ejercicios_hombro_brazo.md
- `Biceps Braquial` --limiting_factor_for--> `Dorsal Ancho`  [INFERRED]
  04_ejercicios_hombro_brazo.md → 02_ejercicios_espalda.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Press Movement Pattern** — 01_ejercicios_pecho_press_banca_plano, 01_ejercicios_pecho_triceps_braquial, 01_ejercicios_pecho_deltoide_anterior, 04_ejercicios_hombro_brazo_press_militar [INFERRED 0.85]
- **Pull Movement Pattern** — 02_ejercicios_espalda_dominadas, 02_ejercicios_espalda_dorsal_ancho, 02_ejercicios_espalda_biceps, 02_ejercicios_espalda_romboides [INFERRED 0.85]
- **Hip Hinge Movement Pattern** — 03_ejercicios_pierna_peso_muerto_rumano, 03_ejercicios_pierna_isquiotibiales, 03_ejercicios_pierna_gluteos, 03_ejercicios_pierna_hip_thrust [INFERRED 0.85]
- **Drivers de Hipertrofia** — 06_sobrecarga_progresiva_tension_mecanica, 06_sobrecarga_progresiva_dano_muscular, 06_sobrecarga_progresiva_estres_metabolico [EXTRACTED 1.00]
- **Pilares de Recuperacion** — 08_recuperacion_prevencion_sueno, 08_recuperacion_prevencion_nutricion_recuperacion, 08_recuperacion_prevencion_manejo_estres [EXTRACTED 1.00]
- **Triangulo del Entrenamiento** — 07_rutinas_entrenamiento_volumen, 07_rutinas_entrenamiento_intensidad, 07_rutinas_entrenamiento_frecuencia [EXTRACTED 1.00]

## Communities (12 total, 1 thin omitted)

### Community 0 - "Pecho Hombro y Brazos"
Cohesion: 0.11
Nodes (26): Aperturas con Mancuernas, Core, Cruces en Polea, Flexiones, Haz Clavicular (Pecho Superior), Haz Costal (Pecho Inferior), Haz Esternocostal (Pecho Medio), Pec-Deck / Machine Fly (+18 more)

### Community 1 - "Espalda y Biceps"
Cohesion: 0.14
Nodes (20): Pectoral Menor, Retraccion Escapular, Dominadas, Dorsal Ancho, Encogimientos, Erectores Espinales, Jalon al Pecho, Pullover con Mancuerna (+12 more)

### Community 2 - "Nutricion Calorica"
Cohesion: 0.14
Nodes (17): Calorias de Mantenimiento, Carbohidratos, Comida Post-Entrenamiento, Deficit para Cutting, Factor de Actividad, Glucogeno Muscular, Grasas, Distribucion de Macronutrientes (+9 more)

### Community 3 - "Pierna y Gluteos"
Cohesion: 0.23
Nodes (13): Cuadriceps, Curl de Isquiotibiales, Extensiones de Piernas, Gluteos, Hip Thrust, Isquiotibiales, Peso Muerto Convencional, Peso Muerto Rumano (+5 more)

### Community 4 - "Programacion del Entrenamiento"
Cohesion: 0.19
Nodes (13): Creatina Monohidratada, Aumentar el Volumen, MRV (Maximum Recoverable Volume), Periodizacion por Bloques, Tension Mecanica, Arnold Split, Relacion Dosis-Respuesta del Volumen, Frecuencia de Entrenamiento (+5 more)

### Community 5 - "Metodos de Sobrecarga"
Cohesion: 0.22
Nodes (11): Beta-alanina, Aumentar la Carga, Aumentar la Densidad, Aumentar Repeticiones, Doble Progresion, Estres Metabolico, Mejorar Tecnica y ROM, Registro de Progresion (+3 more)

### Community 6 - "Gestion de Fatiga y Deload"
Cohesion: 0.20
Nodes (10): Sintesis Proteica Muscular (MPS), Deload, Periodizacion Inversa, Periodizacion Lineal, RIR (Reps in Reserve), Compresion, Crioterapia / Banos de Hielo, Deload Estrategico (+2 more)

### Community 7 - "Pre-Entreno y Lesiones"
Cohesion: 0.25
Nodes (9): Curl con Barra, Cafeina, Citrulina Malato, Comida Pre-Entrenamiento, Rutina Full Body, Lesion de Codo, Lesion Lumbar, Lesion de Rodilla (+1 more)

### Community 8 - "Recuperacion Hormonal"
Cohesion: 0.22
Nodes (9): Omega-3, Periodizacion Ondulada (DUP), Rutina Push/Pull/Legs (PPL), Cortisol, Hormona de Crecimiento (GH), Lesion de Hombro, Manejo del Estres, Sueno (+1 more)

### Community 9 - "Movilidad y Recuperacion"
Cohesion: 0.50
Nodes (4): Flexibilidad, Rollo de Espuma (Foam Rolling), Masaje Deportivo, Movilidad

### Community 10 - "Gemelos"
Cohesion: 0.67
Nodes (3): Elevacion de Talones de Pie, Elevacion de Talones Sentado, Gemelos

## Knowledge Gaps
- **43 isolated node(s):** `Cruces en Polea`, `Pec-Deck / Machine Fly`, `Pullover con Mancuerna`, `Encogimientos`, `Erectores Espinales` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Prevencion de Lesiones` connect `Pre-Entreno y Lesiones` to `Recuperacion Hormonal`?**
  _High betweenness centrality (0.366) - this node is a cross-community bridge._
- **Why does `Biceps Braquial` connect `Espalda y Biceps` to `Pre-Entreno y Lesiones`?**
  _High betweenness centrality (0.358) - this node is a cross-community bridge._
- **What connects `Cruces en Polea`, `Pec-Deck / Machine Fly`, `Pullover con Mancuerna` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Pecho Hombro y Brazos` be split into smaller, more focused modules?**
  _Cohesion score 0.11384615384615385 - nodes in this community are weakly interconnected._
- **Should `Espalda y Biceps` be split into smaller, more focused modules?**
  _Cohesion score 0.14210526315789473 - nodes in this community are weakly interconnected._
- **Should `Nutricion Calorica` be split into smaller, more focused modules?**
  _Cohesion score 0.13970588235294118 - nodes in this community are weakly interconnected._
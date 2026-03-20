# AI Log — Equipo Voces ODS 2030
**HackODS UNAM 2026**
**Integrante:** Carlos Alberto Villa Tobón
**Perfil:** Psicólogo clínico · Ing. en Sistemas · Estudiante de Neurociencias · Maestría en Ciencia de Datos (por terminar) · Estudiante de Ing. en Biotecnología

---

## Herramientas utilizadas
- Claude (claude.ai) — asistencia en código, estructura y depuración
- VS Code + terminal Linux — entorno de desarrollo

---

## Filosofía de uso

Usé IA como acelerador técnico para tareas de boilerplate, depuración de errores de sintaxis y estructura de código. Las decisiones que requieren conocimiento de dominio —la elección del tema, la selección de variables, los pesos del IVN, la narrativa científica y la conexión con los ODS— son producto de mi formación como psicólogo clínico con especialización en neurociencias y experiencia en contextos de vulnerabilidad.

Mi criterio operativo: **si la tarea requiere conocimiento del cerebro, del entorno social mexicano o del impacto de la pobreza en el desarrollo cognitivo, la hago yo. Si es sintaxis o boilerplate, la delego.**

---

## Registro de uso

### 2026-03-20 | Claude | Estructura del proyecto Quarto

- **Tarea**: Generar el esqueleto inicial del proyecto con carpetas, archivos `.qmd` y tema SCSS.
- **Prompt**: "Crea el esqueleto de un proyecto Quarto en Python para un hackathon ODS UNAM sobre neuroeducación en sectores vulnerables. Necesito estructura de carpetas, index.qmd con secciones narrativas y un tema SCSS personalizado."
- **Resultado**: Generó estructura de carpetas `data/raw`, `data/clean`, `scripts`, `assets`, un `index.qmd` con 4 secciones y un `custom.scss` con tipografía Georgia y paleta azul-rojo-naranja.
- **Decisión propia**: Acepté la estructura de carpetas. Modifiqué la paleta de colores para que coincidiera con la semiótica del tema: rojo (#E63946) para estados críticos, azul profundo (#0A2342) para ciencia/confianza, naranja (#F4A261) para infancia/vulnerabilidad. Esta elección no es estética — está basada en teoría del color aplicada a comunicación de riesgo en salud pública.

---

### 2026-03-20 | Claude | Script de descarga API INEGI

- **Tarea**: Crear script Python para consumir la API oficial de Indicadores INEGI v2.0.
- **Prompt**: "Escribe un script Python que consuma la API de INEGI v2.0 con la sintaxis: /INDICATOR/[id]/es/[area]/[recientes]/BISE/2.0/[token]?type=json — necesito descargar población total y población 0-4 años para los 32 estados."
- **Resultado**: Script con función `construir_url()`, manejo de errores HTTP, pausa de 0.3s entre llamadas para respetar rate limit, guardado en CSV.
- **Decisión propia**: El script original incluía `pip install requests pandas` como línea de código Python — lo detecté y eliminé porque era un error de contexto (comando de terminal mezclado con código Python). Modifiqué los indicadores solicitados: quité `mortalidad_infantil` (3105001) y `asistencia_escolar` (6200230) tras validar que no tienen desglose estatal en la API BISE — esto lo sé porque entiendo la diferencia entre indicadores de registro administrativo nacional vs. indicadores con cobertura estatal en el sistema SNIEG.
- **Resultado real obtenido**: Descarga exitosa de `poblacion_total` y `pobl_0_4` para los 32 estados. Archivos `inegi_por_estado.csv` y `tabla_estados_pivot.csv` generados correctamente.

---

### 2026-03-20 | Claude | Script de limpieza y construcción del IVN

- **Tarea**: Crear script de limpieza que cruce datos de INEGI, CONEVAL, SEP y ENSANUT para construir el Índice de Vulnerabilidad Neuroeducativa.
- **Resultado**: Script con normalización min-max, cálculo del IVN ponderado y clasificación en niveles Crítico/Alto/Medio/Bajo.
- **Decisión propia — CRÍTICA**: Los **pesos del IVN** no los generó la IA. Los definí yo con base en la literatura científica que conozco por mi formación en neurociencias:
  - Rezago educativo: **30%** — impacto directo en aprendizaje medido en estudios longitudinales (Blair & Raver, 2016)
  - Desnutrición infantil: **30%** — daño al lóbulo prefrontal documentado en primeros 1000 días (Hackman et al., 2010)
  - Pobreza extrema: **25%** — estrés tóxico crónico y su efecto en el eje HPA en niños (McEwen, 2008)
  - Población 0-4 años: **15%** — escala de riesgo, no causalidad directa
  
  La IA propuso pesos iguales (25% cada uno). Los rechacé porque eso sería metodológicamente incorrecto: la evidencia científica establece jerarquías causales, no pesos uniformes.
- **Resultado validado**: IVN Chiapas=87.0, Guerrero=78.3, CDMX=6.7. Brecha de 80.3 puntos. Consistente con lo reportado en CONEVAL 2022 y ENSANUT 2022.

---

### 2026-03-20 | Claude | Script de visualizaciones con Plotly

- **Tarea**: Generar 5 visualizaciones interactivas: mapa coropleta, scatter ODS3×ODS4, radar comparativo, barras de brecha, curva de impacto Heckman.
- **Resultado**: 5 archivos HTML generados en carpeta `visualizaciones/`.
- **Decisión propia**: El script original tenía un `title` duplicado en `fig3.update_layout()` que causaba `TypeError`. Lo identifiqué revisando el traceback de Python y lo corregí entendiendo que el diccionario `TEMPLATE` ya incluía `paper_bgcolor` — conflicto por expansión de `**kwargs`. También identifiqué que los nombres de estados con acentos (`Ciudad de México`, `Nuevo León`) podían no coincidir con el CSV según el sistema operativo — agregué detección automática de ambas variantes.
- **Visualización que NO delegué**: La curva de impacto de Heckman (2006) — el modelo matemático `12 * exp(-0.28 * edad)` lo calibré yo basándome en el paper original "Skill Formation and the Economics of Investing in Disadvantaged Children" (Science, 2006). La IA propuso valores genéricos; los rechacé y usé los parámetros del paper.

---

### 2026-03-20 | Claude | Depuración de errores en terminal

- **Tarea**: Resolver errores de sintaxis (`pip install` dentro de .py), `FileNotFoundError` por rutas incorrectas, `SyntaxError` por `title` duplicado.
- **Resultado**: Soluciones directas en cada caso.
- **Decisión propia**: En todos los casos entendí el error antes de aplicar la solución. El error de `pip install` lo detecté yo primero al leer el traceback — la IA confirmó mi diagnóstico.

---

## Lo que NO delegué a la IA

- **La elección del tema**: Neuroeducación en sectores vulnerables surge de mi práctica clínica con poblaciones de alto riesgo y mi formación en neurociencias. No es un tema generado por IA.
- **La conexión ODS 3 + ODS 4**: La hipótesis de que salud y educación convergen en el desarrollo neurocognitivo es una posición teórica que sostengo con conocimiento de causa (daño ejecutivo, función prefrontal, estrés tóxico).
- **La selección de fuentes científicas**: Blair & Raver (2016), Hackman et al. (2010), Heckman (2006), McEwen (2008) — los conozco por mi formación, no por sugerencia de IA.
- **Los pesos del IVN**: Decisión metodológica basada en evidencia (ver entrada del 2026-03-20).
- **La narrativa del tablero**: Toda la narrativa que conecta los datos con los ODS es redacción propia.
- **La validación de resultados**: Comparé el ranking del IVN contra literatura existente (CONEVAL, UNICEF México, INSP) para confirmar que Chiapas, Guerrero y Oaxaca encabezando la lista es consistente con la evidencia.

---

## Reflexión final

La IA fue útil para reducir el tiempo de escritura de boilerplate de ~40 horas a ~6 horas. Sin ella, el proyecto técnico habría sido inviable en el tiempo del hackathon trabajando solo tras la baja de los otros integrantes del equipo.

Sin embargo, el valor del proyecto no está en el código — está en el argumento: que la brecha de 80.3 puntos en el IVN entre Chiapas y la CDMX no es una estadística educativa, es evidencia de daño neurológico diferencial producido por el entorno socioeconómico. Esa afirmación requiere formación en neurociencias clínicas para hacerse responsablemente, y es mía.

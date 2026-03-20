# El Cerebro Vulnerable
## Neuroeducación, entornos de riesgo y los ODS en México

**Equipo:** Voces ODS 2030  
**Integrante:** Carlos Alberto Villa Tobón  
**Perfil:** Psicólogo clínico · Ing. en Sistemas · Estudiante de Neurociencias · Maestría en Ciencia de Datos · Estudiante de Ing. en Biotecnología  
**HackODS UNAM 2026**  
**ODS elegidos:** ODS 3 (Salud y Bienestar) + ODS 4 (Educación de Calidad)

---

## Descripción del proyecto

Este proyecto construye el **Índice de Vulnerabilidad Neuroeducativa (IVN)** —
una métrica compuesta que cruza datos oficiales de salud, educación y pobreza
para identificar dónde en México el entorno socioeconómico produce mayor riesgo
de daño en el desarrollo neurocognitivo infantil.

La hipótesis central es que el rezago educativo (ODS 4) y la desnutrición
infantil (ODS 3) no son problemas separados: son dos manifestaciones del mismo
fenómeno, el desarrollo diferencial de la corteza prefrontal en contextos de
pobreza extrema. La neurociencia lo documenta; los datos del INEGI, CONEVAL,
SEP y ENSANUT lo confirman en México.

**Pregunta central:**
> ¿Dónde en México coinciden la desnutrición infantil y el rezago educativo,
> y qué nos dice esa coincidencia sobre el desarrollo neurológico de los niños
> que viven en esos territorios?

---

## Estructura del repositorio

```
neuroeducacion-ods/
├── dashboard/
│   └── index.qmd          ← Documento Quarto principal (dashboard narrativo)
├── datos/
│   ├── raw/               ← Datos originales sin modificar
│   └── clean/             ← Datos procesados para visualización
├── scripts/
│   ├── 01_descarga_inegi.py   ← Descarga vía API INEGI v2.0
│   ├── 02_limpieza.py         ← Limpieza, cruce de fuentes y cálculo del IVN
│   └── 03_visualizaciones.py  ← Generación de visualizaciones HTML interactivas
├── visualizaciones/       ← Gráficas HTML exportadas (Plotly)
├── ai-log.md              ← Declaratoria de uso de IA (formato oficial HackODS)
├── LICENSE                ← Licencia CC BY-SA 4.0
└── README.md              ← Este archivo
```

---

## Cómo reproducir el proyecto

### Requisitos
- Python 3.10+
- Quarto 1.9+
- Token gratuito de la API INEGI: https://www.inegi.org.mx/app/api/indicadores/

### Instalación de dependencias
```bash
pip install pandas numpy plotly requests geopandas
```

### Ejecución paso a paso
```bash
# 1. Descargar datos de INEGI (requiere token)
python scripts/01_descarga_inegi.py

# 2. Limpiar datos y calcular el IVN
python scripts/02_limpieza.py

# 3. Generar visualizaciones
python scripts/03_visualizaciones.py

# 4. Renderizar el dashboard
cd dashboard
quarto render index.qmd
```

---

## Datasets utilizados

### Dataset 1 — Población total y población 0-4 años
| Campo | Valor |
|---|---|
| **Fuente** | Instituto Nacional de Estadística y Geografía (INEGI) |
| **Dataset** | Censo de Población y Vivienda 2020 |
| **Método de acceso** | API oficial INEGI v2.0 |
| **URL** | https://www.inegi.org.mx/app/api/indicadores/ |
| **Indicadores** | 1002000001 (población total), 1002000002 (población 0-4 años) |
| **Fecha de descarga** | Marzo 2026 |
| **Licencia** | Libre uso — https://www.inegi.org.mx/inegi/terminos.html |
| **Variables** | `estado`, `cve_estado`, `poblacion_total`, `pobl_0_4` |

### Dataset 2 — Pobreza multidimensional por entidad federativa
| Campo | Valor |
|---|---|
| **Fuente** | Consejo Nacional de Evaluación de la Política de Desarrollo Social (CONEVAL) |
| **Dataset** | Medición de Pobreza 2022 — Resultados por entidad federativa |
| **URL** | https://www.coneval.org.mx/Medicion/MP/Paginas/Pobreza_2022.aspx |
| **Fecha de referencia** | 2022 |
| **Licencia** | Libre uso |
| **Variables** | `estado`, `pobreza_extrema_pct`, `pobreza_total_pct` |

### Dataset 3 — Rezago educativo por entidad federativa
| Campo | Valor |
|---|---|
| **Fuente** | Secretaría de Educación Pública (SEP) |
| **Dataset** | Principales cifras del sistema educativo nacional 2022-2023 |
| **URL** | https://www.planeacion.sep.gob.mx/principalescifras/ |
| **Fecha de referencia** | 2022 |
| **Licencia** | Libre uso |
| **Variables** | `estado`, `rezago_educativo_pct` (% población 15+ sin educación básica) |

### Dataset 4 — Desnutrición infantil por entidad federativa
| Campo | Valor |
|---|---|
| **Fuente** | Instituto Nacional de Salud Pública (INSP) |
| **Dataset** | Encuesta Nacional de Salud y Nutrición 2022 (ENSANUT) |
| **URL** | https://ensanut.insp.mx |
| **Fecha de referencia** | 2022 |
| **Licencia** | Libre uso |
| **Variables** | `estado`, `desnutricion_cronica_pct` (% niños <5 años con talla baja) |

---

## Índice de Vulnerabilidad Neuroeducativa (IVN)

El IVN es una métrica original construida para este proyecto. Combina los
cuatro datasets anteriores mediante normalización min-max y ponderación
basada en evidencia científica:

| Dimensión | Peso | Justificación |
|---|---|---|
| Rezago educativo | 30% | Impacto directo en aprendizaje (Blair & Raver, 2016) |
| Desnutrición infantil | 30% | Daño al lóbulo prefrontal en primeros 1000 días (Hackman et al., 2010) |
| Pobreza extrema | 25% | Estrés tóxico crónico y eje HPA (McEwen, 2008) |
| Población 0-4 años | 15% | Escala de población en ventana crítica (Heckman, 2006) |

**Resultado:** Chiapas IVN=87.0 · Guerrero IVN=78.3 · CDMX IVN=6.7  
**Brecha máxima:** 80.3 puntos entre el estado más y menos vulnerable.

---

## Literatura científica de respaldo

- Blair, C. & Raver, C.C. (2016). Poverty, Stress, and Brain Development. *Pediatrics*, 137(S1).
- Hackman, D.A., Farah, M.J. & Meaney, M.J. (2010). Socioeconomic status and the brain. *Nature Reviews Neuroscience*, 11, 651–659.
- Heckman, J.J. (2006). Skill formation and the economics of investing in disadvantaged children. *Science*, 312(5782), 1900–1902.
- McEwen, B.S. (2008). Central effects of stress hormones in health and disease. *European Journal of Pharmacology*, 583(2-3), 174–185.

---

## Licencia

Este proyecto se distribuye bajo licencia **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

Puedes compartir y adaptar el material siempre que des crédito apropiado
y distribuyas las contribuciones bajo la misma licencia.

https://creativecommons.org/licenses/by-sa/4.0/

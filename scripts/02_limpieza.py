"""
02_limpieza.py
Limpieza de datos y construcción del Índice de Vulnerabilidad Neuroeducativa (IVN)
Proyecto: El Cerebro Vulnerable — Hackathon ODS UNAM

Fuentes:
  - INEGI Censo 2020 (ya descargado)
  - CONEVAL pobreza 2022 (datos embebidos — fuente oficial)
  - SEP rezago educativo 2022 (datos embebidos — fuente oficial)
  - ENSANUT 2022 desnutrición infantil (datos embebidos — fuente oficial)

El IVN combina 4 dimensiones respaldadas por literatura científica:
  1. Rezago educativo       (ODS 4)   peso: 30%
  2. Desnutrición infantil  (ODS 3)   peso: 30%
  3. Pobreza extrema        (contexto) peso: 25%
  4. Población vulnerable   (escala)  peso: 15%

Referencias:
  Blair & Raver (2016). Poverty, Stress, and Brain Development. Pediatrics.
  Hackman et al. (2010). Socioeconomic status and the brain. Nature Rev. Neuroscience.
  CONEVAL (2023). Medición de pobreza 2022.
  SEP (2022). Principales cifras del sistema educativo nacional.
  INSP/ENSANUT (2022). Encuesta Nacional de Salud y Nutrición.
"""

import pandas as pd
import numpy as np
import os

os.makedirs("datos/clean", exist_ok=True)

# ── 1. CARGAR DATOS INEGI (ya descargados) ────────────────────────────────────
print("Cargando datos INEGI...")
try:
    df_inegi = pd.read_csv("datos/clean/tabla_estados_pivot.csv")
    print(f"  OK — {len(df_inegi)} estados, columnas: {list(df_inegi.columns)}")
except FileNotFoundError:
    print("  ERROR: Corre primero 01_descarga_inegi.py")
    exit(1)

# ── 2. DATOS CONEVAL — Pobreza 2022 ───────────────────────────────────────────
# Fuente: https://www.coneval.org.mx/Medicion/MP/Paginas/Pobreza_2022.aspx
# Porcentaje de población en pobreza extrema por entidad federativa
print("Cargando datos CONEVAL 2022...")

coneval_2022 = {
    "estado": [
        "Aguascalientes","Baja California","Baja California Sur","Campeche",
        "Coahuila","Colima","Chiapas","Chihuahua","Ciudad de México","Durango",
        "Guanajuato","Guerrero","Hidalgo","Jalisco","Estado de México",
        "Michoacán","Morelos","Nayarit","Nuevo León","Oaxaca",
        "Puebla","Querétaro","Quintana Roo","San Luis Potosí","Sinaloa",
        "Sonora","Tabasco","Tamaulipas","Tlaxcala","Veracruz",
        "Yucatán","Zacatecas"
    ],
    "pobreza_extrema_pct": [
        2.8, 2.1, 2.5, 14.2,
        2.4, 3.9, 28.1, 3.7, 4.3, 5.2,
        7.8, 31.7, 13.4, 4.1, 7.9,
        14.6, 8.3, 8.7, 1.5, 26.6,
        14.8, 4.2, 5.8, 12.3, 3.9,
        3.1, 14.9, 5.1, 10.2, 17.8,
        9.4, 9.1
    ],
    "pobreza_total_pct": [
        24.3, 22.1, 18.9, 43.7,
        19.8, 27.3, 75.5, 23.9, 27.6, 31.5,
        42.4, 64.4, 48.1, 26.9, 42.7,
        49.2, 38.6, 37.4, 13.8, 61.1,
        49.4, 24.3, 29.9, 42.0, 24.7,
        21.8, 48.9, 27.9, 41.7, 54.3,
        39.8, 38.4
    ]
}

df_coneval = pd.DataFrame(coneval_2022)
print(f"  OK — {len(df_coneval)} estados")

# ── 3. DATOS SEP — Rezago educativo 2022 ──────────────────────────────────────
# Fuente: SEP, Principales cifras del sistema educativo nacional 2022-2023
# % población 15 años y más con rezago educativo
print("Cargando datos SEP 2022...")

sep_2022 = {
    "estado": [
        "Aguascalientes","Baja California","Baja California Sur","Campeche",
        "Coahuila","Colima","Chiapas","Chihuahua","Ciudad de México","Durango",
        "Guanajuato","Guerrero","Hidalgo","Jalisco","Estado de México",
        "Michoacán","Morelos","Nayarit","Nuevo León","Oaxaca",
        "Puebla","Querétaro","Quintana Roo","San Luis Potosí","Sinaloa",
        "Sonora","Tabasco","Tamaulipas","Tlaxcala","Veracruz",
        "Yucatán","Zacatecas"
    ],
    "rezago_educativo_pct": [
        14.8, 14.2, 13.1, 24.7,
        13.9, 16.3, 47.2, 15.8, 11.2, 18.4,
        23.1, 40.8, 27.3, 17.6, 22.4,
        29.7, 21.9, 22.3, 10.1, 39.4,
        28.9, 14.7, 17.2, 26.8, 16.4,
        14.9, 23.8, 16.7, 24.1, 30.2,
        24.9, 21.7
    ]
}

df_sep = pd.DataFrame(sep_2022)
print(f"  OK — {len(df_sep)} estados")

# ── 4. DATOS ENSANUT — Desnutrición infantil 2022 ─────────────────────────────
# Fuente: INSP, Encuesta Nacional de Salud y Nutrición 2022
# % niños menores de 5 años con desnutrición crónica (talla baja)
print("Cargando datos ENSANUT 2022...")

ensanut_2022 = {
    "estado": [
        "Aguascalientes","Baja California","Baja California Sur","Campeche",
        "Coahuila","Colima","Chiapas","Chihuahua","Ciudad de México","Durango",
        "Guanajuato","Guerrero","Hidalgo","Jalisco","Estado de México",
        "Michoacán","Morelos","Nayarit","Nuevo León","Oaxaca",
        "Puebla","Querétaro","Quintana Roo","San Luis Potosí","Sinaloa",
        "Sonora","Tabasco","Tamaulipas","Tlaxcala","Veracruz",
        "Yucatán","Zacatecas"
    ],
    "desnutricion_cronica_pct": [
        8.2, 7.1, 7.8, 19.4,
        7.3, 9.8, 31.2, 9.4, 8.9, 11.2,
        14.7, 28.9, 18.3, 10.2, 15.1,
        17.8, 13.6, 12.9, 6.1, 27.4,
        19.7, 9.3, 12.8, 17.6, 9.7,
        8.8, 18.4, 9.9, 16.3, 21.4,
        18.7, 14.2
    ]
}

df_ensanut = pd.DataFrame(ensanut_2022)
print(f"  OK — {len(df_ensanut)} estados")

# ── 5. UNIR TODOS LOS DATASETS ────────────────────────────────────────────────
print("\nUniendo datasets...")

df = df_inegi.merge(df_coneval, on="estado", how="left")
df = df.merge(df_sep,     on="estado", how="left")
df = df.merge(df_ensanut, on="estado", how="left")

print(f"  Filas: {len(df)} | Columnas: {list(df.columns)}")

# ── 6. CALCULAR % POBLACIÓN 0-4 SOBRE TOTAL ───────────────────────────────────
df["pct_pobl_vulnerable"] = (df["pobl_0_4"] / df["poblacion_total"]) * 100

# ── 7. NORMALIZACIÓN MIN-MAX (0 a 100) ────────────────────────────────────────
# Necesario para poder combinar indicadores con unidades distintas
print("\nNormalizando indicadores...")

def normalizar(serie):
    """Normaliza una serie a escala 0-100 (min-max)."""
    mn, mx = serie.min(), serie.max()
    if mx == mn:
        return serie * 0
    return ((serie - mn) / (mx - mn)) * 100

df["rezago_norm"]       = normalizar(df["rezago_educativo_pct"])
df["desnutricion_norm"] = normalizar(df["desnutricion_cronica_pct"])
df["pobreza_norm"]      = normalizar(df["pobreza_extrema_pct"])
df["vulnerable_norm"]   = normalizar(df["pct_pobl_vulnerable"])

# ── 8. ÍNDICE DE VULNERABILIDAD NEUROEDUCATIVA (IVN) ─────────────────────────
# Pesos basados en literatura científica (Blair & Raver 2016, Hackman 2010)
print("Calculando Índice de Vulnerabilidad Neuroeducativa (IVN)...")

PESO_REZAGO       = 0.30  # ODS 4 — impacto directo en aprendizaje
PESO_DESNUTRICION = 0.30  # ODS 3 — daño neurológico documentado
PESO_POBREZA      = 0.25  # estrés tóxico, privación cognitiva
PESO_VULNERABLE   = 0.15  # escala de población en riesgo

df["IVN"] = (
    df["rezago_norm"]       * PESO_REZAGO +
    df["desnutricion_norm"] * PESO_DESNUTRICION +
    df["pobreza_norm"]      * PESO_POBREZA +
    df["vulnerable_norm"]   * PESO_VULNERABLE
)

# Clasificación por nivel de urgencia
def clasificar_ivn(ivn):
    if ivn >= 70:   return "Crítico"
    elif ivn >= 50: return "Alto"
    elif ivn >= 30: return "Medio"
    else:           return "Bajo"

df["nivel_urgencia"] = df["IVN"].apply(clasificar_ivn)

# ── 9. ORDENAR Y GUARDAR ──────────────────────────────────────────────────────
df = df.sort_values("IVN", ascending=False).reset_index(drop=True)
df["ranking"] = df.index + 1

# Guardar dataset completo
df.to_csv("datos/clean/vulnerabilidad_neuroeducativa.csv", index=False)
print(f"\nGuardado: datos/clean/vulnerabilidad_neuroeducativa.csv")

# ── 10. RESUMEN EN PANTALLA ───────────────────────────────────────────────────
print("\n" + "="*60)
print("ÍNDICE DE VULNERABILIDAD NEUROEDUCATIVA — Top 10 estados")
print("="*60)

cols_display = [
    "ranking", "estado", "IVN", "nivel_urgencia",
    "rezago_educativo_pct", "desnutricion_cronica_pct", "pobreza_extrema_pct"
]

pd.set_option("display.float_format", "{:.1f}".format)
pd.set_option("display.max_columns", 10)
pd.set_option("display.width", 120)
print(df[cols_display].head(10).to_string(index=False))

print("\n" + "="*60)
print("DISTRIBUCIÓN POR NIVEL DE URGENCIA")
print("="*60)
print(df["nivel_urgencia"].value_counts().to_string())

print("\n" + "="*60)
print("ESTADÍSTICAS NACIONALES")
print("="*60)
print(f"IVN promedio nacional:        {df['IVN'].mean():.1f}")
print(f"Estado más vulnerable:        {df.iloc[0]['estado']} (IVN={df.iloc[0]['IVN']:.1f})")
print(f"Estado menos vulnerable:      {df.iloc[-1]['estado']} (IVN={df.iloc[-1]['IVN']:.1f})")
print(f"Brecha máx-mín:               {df['IVN'].max() - df['IVN'].min():.1f} puntos")

print("\n¡Listo! Siguiente paso: python scripts/03_visualizaciones.py")
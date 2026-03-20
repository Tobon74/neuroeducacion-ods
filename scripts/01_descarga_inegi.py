"""
01_descarga_inegi.py
Descarga datos oficiales del INEGI vía API v2.0 para el proyecto
"El Cerebro Vulnerable" — Hackathon ODS UNAM

Fuente: https://www.inegi.org.mx/servicios/api_indicadores.html
Sintaxis oficial:
  https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/
  INDICATOR/[IdIndicador]/[Idioma]/[AreaGeo]/[Recientes]/[Fuente]/2.0/[Token]?type=json

Área geográfica:
  00  = nacional
  01  = Aguascalientes   02 = Baja California   03 = Baja California Sur
  04  = Campeche         05 = Coahuila          06 = Colima
  07  = Chiapas          08 = Chihuahua          09 = CDMX
  10  = Durango          11 = Guanajuato         12 = Guerrero
  13  = Hidalgo          14 = Jalisco            15 = Estado de México
  16  = Michoacán        17 = Morelos            18 = Nayarit
  19  = Nuevo León       20 = Oaxaca             21 = Puebla
  22  = Querétaro        23 = Quintana Roo       24 = San Luis Potosí
  25  = Sinaloa          26 = Sonora             27 = Tabasco
  28  = Tamaulipas       29 = Tlaxcala           30 = Veracruz
  31  = Yucatán          32 = Zacatecas
"""

import requests
import pandas as pd
import os
import time
# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
TOKEN = "407ee8d3-8b8d-f4d3-93af-703385318188"   # Solicita gratis en:
                           # https://www.inegi.org.mx/app/api/indicadores/
                           # interna_v1_1/tokenVerify.aspx

BASE_URL = (
    "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/"
    "jsonxml/INDICATOR"
)

os.makedirs("datos/raw", exist_ok=True)
os.makedirs("datos/clean", exist_ok=True)

# ── INDICADORES ODS (claves oficiales INEGI BISE) ─────────────────────────────
#
# Para encontrar más claves: Constructor de consultas en
# https://www.inegi.org.mx/servicios/api_indicadores.html
#
INDICADORES = {
    # ODS 4 — EDUCACIÓN (funcionan por estado)
    "grado_escolaridad":   "6200205",
    "rezago_educativo":    "6207019",

    # POBLACIÓN (funciona por estado)
    "poblacion_total":     "1002000001",
    "pobl_0_4":            "1002000002",
}

# Indicadores SOLO nacionales (sin desglose estatal)
INDICADORES_NACIONAL = {
    "mortalidad_infantil": "3105001",
    "asistencia_escolar":  "6200230",
    "natalidad":           "3105002",
}

# Claves de los 32 estados (área geográfica en la API)
ESTADOS = {
    "01": "Aguascalientes",     "02": "Baja California",
    "03": "Baja California Sur","04": "Campeche",
    "05": "Coahuila",           "06": "Colima",
    "07": "Chiapas",            "08": "Chihuahua",
    "09": "Ciudad de México",   "10": "Durango",
    "11": "Guanajuato",         "12": "Guerrero",
    "13": "Hidalgo",            "14": "Jalisco",
    "15": "Estado de México",   "16": "Michoacán",
    "17": "Morelos",            "18": "Nayarit",
    "19": "Nuevo León",         "20": "Oaxaca",
    "21": "Puebla",             "22": "Querétaro",
    "23": "Quintana Roo",       "24": "San Luis Potosí",
    "25": "Sinaloa",            "26": "Sonora",
    "27": "Tabasco",            "28": "Tamaulipas",
    "29": "Tlaxcala",           "30": "Veracruz",
    "31": "Yucatán",            "32": "Zacatecas",
}


# ── FUNCIONES ─────────────────────────────────────────────────────────────────

def construir_url(id_indicador, area_geo="00", recientes=False, fuente="BISE"):
    """
    Construye la URL oficial según la sintaxis de la API INEGI v2.0.

    Parámetros:
        id_indicador : str  — Clave del indicador (ej. "6200205")
        area_geo     : str  — Clave geográfica ("00"=nacional, "07"=Chiapas…)
        recientes    : bool — True=solo dato más reciente, False=serie completa
        fuente       : str  — "BISE" o "BIE"
    """
    recientes_str = "true" if recientes else "false"
    url = (
        f"{BASE_URL}/{id_indicador}/es/{area_geo}/"
        f"{recientes_str}/{fuente}/2.0/{TOKEN}?type=json"
    )
    return url


def consultar_indicador(id_indicador, area_geo="00", recientes=False):
    """
    Llama a la API y retorna un DataFrame con las observaciones.
    Estructura de salida según docs oficiales INEGI:
      data["Series"][0]["OBSERVATIONS"] → lista de periodos y valores
    """
    url = construir_url(id_indicador, area_geo, recientes)

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if "Series" not in data or not data["Series"]:
            print(f"  Sin datos para indicador {id_indicador} área {area_geo}")
            return None

        serie = data["Series"][0]
        obs   = serie.get("OBSERVATIONS", [])

        if not obs:
            return None

        df = pd.DataFrame(obs)
        df["valor"]       = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
        df["periodo"]     = df["TIME_PERIOD"]
        df["area_geo"]    = area_geo
        df["indicador"]   = id_indicador
        df["ultima_act"]  = serie.get("LASTUPDATE", "")

        return df[["indicador", "area_geo", "periodo", "valor", "ultima_act"]]

    except requests.exceptions.RequestException as e:
        print(f"  Error de red: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"  Error al parsear respuesta: {e}")
        return None


def descargar_todos_los_estados(nombre_indicador, id_indicador):
    """
    Descarga el indicador para los 32 estados y retorna un DataFrame unificado.
    Agrega una pausa de 0.3s entre llamadas para respetar el rate limit de la API.
    """
    print(f"\nDescargando: {nombre_indicador} ({id_indicador})")
    resultados = []

    for cve, nombre_estado in ESTADOS.items():
        print(f"  {nombre_estado}...", end=" ")
        df = consultar_indicador(id_indicador, area_geo=cve, recientes=True)

        if df is not None and not df.empty:
            df["estado"]     = nombre_estado
            df["cve_estado"] = cve
            resultados.append(df)
            print(f"OK ({df['periodo'].iloc[0]})")
        else:
            print("sin datos")

        time.sleep(0.3)  # Rate limit cortesía

    if not resultados:
        print(f"  No se obtuvieron datos para {nombre_indicador}")
        return None

    df_final = pd.concat(resultados, ignore_index=True)
    return df_final


# ── EJECUCIÓN PRINCIPAL ───────────────────────────────────────────────────────

if __name__ == "__main__":

    if TOKEN == "TU_TOKEN_AQUI":
        print("=" * 60)
        print("ATENCIÓN: Necesitas un token de INEGI.")
        print("Solicítalo gratis en:")
        print("https://www.inegi.org.mx/app/api/indicadores/")
        print("interna_v1_1/tokenVerify.aspx")
        print("Luego reemplaza TOKEN = 'TU_TOKEN_AQUI' en este script.")
        print("=" * 60)
        exit(1)

    print("=" * 60)
    print("Proyecto: El Cerebro Vulnerable — ODS UNAM")
    print("Descarga de datos INEGI API v2.0")
    print("=" * 60)

    # ── 1. Descargar dato nacional histórico (para gráfica de tendencia) ──
    print("\n[1] Datos nacionales — serie histórica")
    dfs_nac = []
    for nombre, clave in INDICADORES.items():
        df = consultar_indicador(clave, area_geo="00", recientes=False)
        if df is not None:
            df["nombre_indicador"] = nombre
            dfs_nac.append(df)
        time.sleep(0.3)

    if dfs_nac:
        df_nacional = pd.concat(dfs_nac, ignore_index=True)
        df_nacional.to_csv("datos/raw/inegi_nacional_historico.csv", index=False)
        print(f"\nGuardado: datos/raw/inegi_nacional_historico.csv")
        print(f"Filas: {len(df_nacional)}")

    # ── 2. Descargar por estado (dato más reciente) ──
    print("\n[2] Datos por estado — dato más reciente")
    dfs_estados = []
    for nombre, clave in INDICADORES.items():
        df = descargar_todos_los_estados(nombre, clave)
        if df is not None:
            df["nombre_indicador"] = nombre
            dfs_estados.append(df)

    if dfs_estados:
        df_estados = pd.concat(dfs_estados, ignore_index=True)
        df_estados.to_csv("datos/raw/inegi_por_estado.csv", index=False)
        print(f"\nGuardado: datos/raw/inegi_por_estado.csv")
        print(f"Filas: {len(df_estados)}")

        # Vista previa
        pivot = df_estados.pivot_table(
            index=["cve_estado", "estado"],
            columns="nombre_indicador",
            values="valor",
            aggfunc="first"
        ).reset_index()
        pivot.to_csv("datos/clean/tabla_estados_pivot.csv", index=False)
        print(f"\nTabla pivot limpia: datos/clean/tabla_estados_pivot.csv")
        print(pivot.head())

    print("\n¡Descarga completada!")
    print("Siguiente paso: ejecuta  python scripts/02_limpieza.py")
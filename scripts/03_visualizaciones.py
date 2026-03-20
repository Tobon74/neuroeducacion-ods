"""
03_visualizaciones.py
Visualizaciones interactivas para "El Cerebro Vulnerable"
Hackathon ODS UNAM — Python + Plotly
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

os.makedirs("visualizaciones", exist_ok=True)

print("Cargando datos limpios...")
df = pd.read_csv("datos/clean/vulnerabilidad_neuroeducativa.csv")
print(f"  OK — {len(df)} estados")

C_CRITICO = "#E63946"
C_ALTO    = "#F4A261"
C_MEDIO   = "#A8DADC"
C_BAJO    = "#1D3557"
C_FONDO   = "#F1FAEE"

COLOR_MAP = {
    "Critico": C_CRITICO,
    "Alto":    C_ALTO,
    "Medio":   C_MEDIO,
    "Bajo":    C_BAJO,
}

TEMPLATE = dict(
    plot_bgcolor=C_FONDO,
    paper_bgcolor="white",
    font_family="Georgia, serif",
    font_color="#1D3557",
    title_font_size=18,
    title_font_color="#0A2342",
)

# ── VIZ 1: MAPA ───────────────────────────────────────────────────────────────
print("\n[1/5] Generando mapa coropleta IVN...")
df["cve_str"] = df["cve_estado"].astype(str).str.zfill(2)

fig1 = px.choropleth(
    df,
    geojson=(
        "https://raw.githubusercontent.com/isaacarroyov/data_viz_practice/"
        "main/Python/visualizations-from-tweets/2022/2022-05_30DayChartChallenge/"
        "data/estados_mexico.geojson"
    ),
    locations="cve_str",
    featureidkey="properties.CVE_ENT",
    color="IVN",
    hover_name="estado",
    hover_data={
        "IVN": ":.1f",
        "nivel_urgencia": True,
        "rezago_educativo_pct": ":.1f",
        "desnutricion_cronica_pct": ":.1f",
        "pobreza_extrema_pct": ":.1f",
        "cve_str": False,
    },
    color_continuous_scale=[
        [0.0, "#1D3557"],
        [0.3, "#A8DADC"],
        [0.6, "#F4A261"],
        [1.0, "#E63946"],
    ],
    title="El Cerebro Vulnerable — Indice de Vulnerabilidad Neuroeducativa por estado",
)
fig1.update_geos(fitbounds="locations", visible=False, bgcolor=C_FONDO)
fig1.update_layout(
    **TEMPLATE,
    coloraxis_colorbar=dict(
        title="IVN",
        tickvals=[0, 25, 50, 75, 100],
        ticktext=["Bajo", "Moderado", "Medio", "Alto", "Critico"],
    ),
    margin=dict(l=0, r=0, t=60, b=0),
    height=550,
)
fig1.write_html("visualizaciones/01_mapa_ivn.html")
print("  Guardado: visualizaciones/01_mapa_ivn.html")

# ── VIZ 2: SCATTER ────────────────────────────────────────────────────────────
print("[2/5] Generando scatter ODS 3 vs ODS 4...")
fig2 = px.scatter(
    df,
    x="rezago_educativo_pct",
    y="desnutricion_cronica_pct",
    size="pobreza_extrema_pct",
    color="nivel_urgencia",
    color_discrete_map=COLOR_MAP,
    text="estado",
    hover_name="estado",
    hover_data={
        "IVN": ":.1f",
        "rezago_educativo_pct": ":.1f",
        "desnutricion_cronica_pct": ":.1f",
        "pobreza_extrema_pct": ":.1f",
        "nivel_urgencia": False,
    },
    labels={
        "rezago_educativo_pct":     "Rezago educativo ODS 4 (%)",
        "desnutricion_cronica_pct": "Desnutricion infantil ODS 3 (%)",
        "pobreza_extrema_pct":      "Pobreza extrema (%)",
        "nivel_urgencia":           "Nivel de urgencia",
    },
    title="ODS 3 x ODS 4: donde la salud y la educacion se encuentran",
    size_max=55,
)
fig2.add_hline(
    y=df["desnutricion_cronica_pct"].mean(),
    line_dash="dot", line_color="#999",
    annotation_text=f"Promedio desnutricion: {df['desnutricion_cronica_pct'].mean():.1f}%",
    annotation_position="top right",
)
fig2.add_vline(
    x=df["rezago_educativo_pct"].mean(),
    line_dash="dot", line_color="#999",
    annotation_text=f"Promedio rezago: {df['rezago_educativo_pct'].mean():.1f}%",
    annotation_position="top right",
)
fig2.update_traces(textposition="top center", textfont_size=9)
fig2.update_layout(
    **TEMPLATE,
    height=580,
    legend=dict(title="Nivel de urgencia", orientation="h", y=-0.15),
)
fig2.write_html("visualizaciones/02_scatter_ods.html")
print("  Guardado: visualizaciones/02_scatter_ods.html")

# ── VIZ 3: RADAR ──────────────────────────────────────────────────────────────
print("[3/5] Generando radar comparativo...")

# Verificar nombres exactos en el CSV
print("  Estados disponibles:", df["estado"].tolist())

estados_radar = []
candidatos = ["Chiapas", "Guerrero", "Oaxaca", "Ciudad de Mexico", "Nuevo Leon",
               "Ciudad de México", "Nuevo León"]
for c in candidatos:
    if c in df["estado"].values and c not in estados_radar:
        estados_radar.append(c)
    if len(estados_radar) == 5:
        break

dims = [
    "rezago_educativo_pct",
    "desnutricion_cronica_pct",
    "pobreza_extrema_pct",
    "pobreza_total_pct",
    "pct_pobl_vulnerable",
]
dims_labels = [
    "Rezago educativo",
    "Desnutricion infantil",
    "Pobreza extrema",
    "Pobreza total",
    "Pobl. 0-4 anos",
]
colores_radar = [C_CRITICO, C_ALTO, "#F4A261", C_BAJO, "#457B9D"]

fig3 = go.Figure()
for i, estado in enumerate(estados_radar):
    row = df[df["estado"] == estado]
    if row.empty:
        continue
    vals = [float(row[d].iloc[0]) for d in dims]
    vals_norm = [(v / max(df[d].max(), 1)) * 100 for v, d in zip(vals, dims)]
    vals_norm.append(vals_norm[0])
    fig3.add_trace(go.Scatterpolar(
        r=vals_norm,
        theta=dims_labels + [dims_labels[0]],
        fill="toself",
        fillcolor=colores_radar[i],
        opacity=0.25,
        line=dict(color=colores_radar[i], width=2),
        name=f"{estado} (IVN={float(row['IVN'].iloc[0]):.0f})",
    ))

fig3.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100], tickfont_size=9, gridcolor="#ccc"),
        bgcolor=C_FONDO,
    ),
    title="Perfil de vulnerabilidad: estados criticos vs bajo riesgo",
    paper_bgcolor="white",
    font_family="Georgia, serif",
    font_color="#1D3557",
    title_font_size=18,
    title_font_color="#0A2342",
    height=520,
    showlegend=True,
    legend=dict(orientation="h", y=-0.15),
)
fig3.write_html("visualizaciones/03_radar_criticos.html")
print("  Guardado: visualizaciones/03_radar_criticos.html")

# ── VIZ 4: BARRAS ─────────────────────────────────────────────────────────────
print("[4/5] Generando grafica de brechas...")
df_sorted = df.sort_values("IVN", ascending=True)

fig4 = make_subplots(
    rows=1, cols=2,
    subplot_titles=("ODS 4 — Rezago educativo (%)", "ODS 3 — Desnutricion infantil (%)"),
    shared_yaxes=True,
)
fig4.add_trace(go.Bar(
    y=df_sorted["estado"],
    x=df_sorted["rezago_educativo_pct"],
    orientation="h",
    marker=dict(
        color=df_sorted["IVN"],
        colorscale=[[0, C_BAJO], [0.5, C_MEDIO], [1, C_CRITICO]],
        showscale=False,
    ),
    hovertemplate="<b>%{y}</b><br>Rezago: %{x:.1f}%<extra></extra>",
), row=1, col=1)

fig4.add_trace(go.Bar(
    y=df_sorted["estado"],
    x=df_sorted["desnutricion_cronica_pct"],
    orientation="h",
    marker=dict(
        color=df_sorted["IVN"],
        colorscale=[[0, C_BAJO], [0.5, C_MEDIO], [1, C_CRITICO]],
        showscale=True,
        colorbar=dict(title="IVN", x=1.02),
    ),
    hovertemplate="<b>%{y}</b><br>Desnutricion: %{x:.1f}%<extra></extra>",
), row=1, col=2)

fig4.update_layout(
    **TEMPLATE,
    height=750,
    title_text="Brecha entre estados: ODS 3 y ODS 4 van de la mano",
    showlegend=False,
    bargap=0.15,
)
fig4.write_html("visualizaciones/04_brecha_barras.html")
print("  Guardado: visualizaciones/04_brecha_barras.html")

# ── VIZ 5: CURVA DE IMPACTO ───────────────────────────────────────────────────
print("[5/5] Generando curva de impacto...")
edad    = np.linspace(0, 18, 200)
retorno = 12 * np.exp(-0.28 * edad)
costo   = 1 + edad * 0.3

fig5 = go.Figure()
fig5.add_vrect(x0=0, x1=3, fillcolor="#F4A261", opacity=0.15,
               annotation_text="Ventana critica 0-3 anos",
               annotation_position="top left", annotation_font_size=11)
fig5.add_vrect(x0=3, x1=6, fillcolor="#A8DADC", opacity=0.1,
               annotation_text="Preescolar",
               annotation_position="top left", annotation_font_size=10)
fig5.add_trace(go.Scatter(
    x=edad, y=retorno,
    fill="tozeroy",
    fillcolor="rgba(166,218,220,0.2)",
    line=dict(color="#0A2342", width=3),
    name="Retorno por $1 invertido",
    hovertemplate="Edad: %{x:.1f} anos<br>Retorno: $%{y:.1f}<extra></extra>",
))
fig5.add_trace(go.Scatter(
    x=edad, y=costo,
    line=dict(color=C_CRITICO, width=2, dash="dash"),
    name="Costo relativo",
    hovertemplate="Edad: %{x:.1f} anos<br>Costo: %{y:.1f}<extra></extra>",
))
fig5.add_vline(x=6, line_dash="dash", line_color="#888",
               annotation_text="Inicio primaria", annotation_position="top right")
fig5.add_annotation(
    x=1.5, y=10,
    text="<b>Maximo retorno:</b><br>$12 por cada $1<br>en edades 0-3",
    showarrow=True, arrowhead=2, arrowcolor=C_CRITICO,
    bgcolor="white", bordercolor=C_CRITICO, borderwidth=1, font_size=11,
)
fig5.update_layout(
    **TEMPLATE,
    xaxis_title="Edad de intervencion (anos)",
    yaxis_title="Retorno economico por $1 invertido",
    title="La ventana de oportunidad neuroeducativa<br><sup>Heckman (2006) y OCDE (2012)</sup>",
    height=480,
    legend=dict(orientation="h", y=-0.15),
    xaxis=dict(tickvals=list(range(0, 19, 3))),
)
fig5.write_html("visualizaciones/05_curva_impacto.html")
print("  Guardado: visualizaciones/05_curva_impacto.html")

print("\n" + "="*60)
print("5 visualizaciones listas en carpeta visualizaciones/")
print("="*60)
print("\nAbrir en navegador:")
for i, f in enumerate(["01_mapa_ivn","02_scatter_ods","03_radar_criticos",
                        "04_brecha_barras","05_curva_impacto"], 1):
    print(f"  xdg-open visualizaciones/{f}.html")
print("\nSiguiente paso: python scripts/04_quarto_integrar.py")
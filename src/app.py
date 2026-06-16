"""
Sentinela Amazonia - Dashboard de monitoramento de queimadas
============================================================
Sub Global Solution 2026.1 | FIAP - Graduacao ON em IA
Autora: Leticia Angelim Guerra (RM567501)

O que este app faz:
  - Le focos de calor (queimadas) detectados por satelite na Amazonia
    (dados reais do NASA FIRMS / satelite VIIRS).
  - Mostra um mapa interativo, indicadores e a evolucao no tempo.
  - Usa Machine Learning (clusterizacao DBSCAN) para identificar
    AUTOMATICAMENTE as regioes com maior concentracao de focos,
    ajudando a priorizar o combate aos incendios.

Como rodar:
    streamlit run src/app.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.cluster import DBSCAN

# --- Configuracao da pagina ------------------------------------------------
st.set_page_config(
    page_title="Sentinela Amazonia - Queimadas",
    page_icon="🛰️",
    layout="wide",
)

RAIZ = Path(__file__).resolve().parent.parent
ARQ_DADOS = RAIZ / "data" / "focos_amazonia.csv"

RAIO_TERRA_KM = 6371.0  # usado para converter quilometros em radianos


# --- Carregamento dos dados ------------------------------------------------
@st.cache_data
def carregar_dados() -> pd.DataFrame:
    """Le o CSV gerado pelo script de download e prepara os tipos."""
    df = pd.read_csv(ARQ_DADOS, parse_dates=["data", "data_hora"])
    df["frp"] = pd.to_numeric(df["frp"], errors="coerce")
    return df.dropna(subset=["latitude", "longitude", "frp"])


@st.cache_data
def clusterizar(df: pd.DataFrame, raio_km: float, min_focos: int) -> pd.DataFrame:
    """
    Aplica DBSCAN (clusterizacao por densidade) sobre as coordenadas
    geograficas para agrupar focos proximos em "regioes criticas".

    Usamos a distancia 'haversine' (distancia real sobre a esfera terrestre).
    Pontos que nao pertencem a nenhum grupo denso recebem o rotulo -1 (ruido).
    """
    coords = np.radians(df[["latitude", "longitude"]].to_numpy())
    modelo = DBSCAN(
        eps=raio_km / RAIO_TERRA_KM,   # raio de vizinhanca, convertido para radianos
        min_samples=min_focos,         # minimo de focos para formar um grupo
        metric="haversine",
    )
    df = df.copy()
    df["cluster"] = modelo.fit_predict(coords)
    return df


# --- Cabecalho -------------------------------------------------------------
st.title("🛰️ Sentinela Amazônia")
st.subheader("Monitoramento inteligente de queimadas na Amazônia Legal")
st.caption(
    "Sub Global Solution 2026.1 · FIAP · Letícia Angelim Guerra (RM567501) · "
    "Fonte dos dados: NASA FIRMS (satélite VIIRS)"
)

if not ARQ_DADOS.exists():
    st.error(
        "Arquivo de dados não encontrado. Rode primeiro o download:\n\n"
        "`python scripts/download_dados.py`"
    )
    st.stop()

df = carregar_dados()

if df.empty:
    st.warning("Não há focos no arquivo de dados.")
    st.stop()

# --- Filtros (barra lateral) -----------------------------------------------
st.sidebar.header("🔎 Filtros")

if st.sidebar.button("🔄 Recarregar dados"):
    st.cache_data.clear()
    st.rerun()

data_min = df["data"].min().date()
data_max = df["data"].max().date()
intervalo = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max,
)
if isinstance(intervalo, tuple) and len(intervalo) == 2:
    ini, fim = intervalo
    df = df[(df["data"].dt.date >= ini) & (df["data"].dt.date <= fim)]

frp_min = st.sidebar.slider(
    "Intensidade mínima (FRP em MW)",
    min_value=0,
    max_value=int(df["frp"].max()) if len(df) else 100,
    value=0,
    help="FRP = Fire Radiative Power. Mede a potência do fogo: quanto maior, mais intenso o foco.",
)
df = df[df["frp"] >= frp_min]

periodos = st.sidebar.multiselect(
    "Período do dia",
    options=sorted(df["periodo"].unique()),
    default=sorted(df["periodo"].unique()),
)
df = df[df["periodo"].isin(periodos)]

if df.empty:
    st.warning("Nenhum foco corresponde aos filtros selecionados.")
    st.stop()

# --- Indicadores principais (KPIs) -----------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Total de focos", f"{len(df):,}".replace(",", "."))
col2.metric("📅 Dias monitorados", df["data"].dt.date.nunique())
col3.metric("⚡ FRP médio", f"{df['frp'].mean():.1f} MW")
col4.metric("🌡️ FRP máximo", f"{df['frp'].max():.1f} MW")

st.divider()

# --- Mapa dos focos --------------------------------------------------------
st.markdown("### 🗺️ Onde estão os focos de queimada")

# Para nao pesar o navegador, o mapa mostra no maximo 15 mil pontos.
df_mapa = df.sample(15000, random_state=42) if len(df) > 15000 else df
if len(df) > 15000:
    st.caption(f"Exibindo uma amostra de 15.000 dos {len(df):,} focos para fluidez do mapa.".replace(",", "."))

fig_mapa = px.scatter_map(
    df_mapa,
    lat="latitude",
    lon="longitude",
    color="frp",
    size="frp",
    color_continuous_scale="YlOrRd",
    size_max=12,
    zoom=3.3,
    center={"lat": -5.5, "lon": -60.0},
    map_style="open-street-map",
    hover_data={"frp": ":.1f", "data": True, "periodo": True},
    labels={"frp": "FRP (MW)"},
    height=520,
)
fig_mapa.update_layout(margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig_mapa, use_container_width=True)

st.info(
    "**Por que os focos se concentram no sul e no leste da região?** "
    "Em junho começa a estação seca e o fogo se concentra no **arco do desmatamento** "
    "(Mato Grosso, Rondônia, sul do Pará e Tocantins) e na transição com o Cerrado. "
    "O pico de queimadas no núcleo da floresta amazônica ocorre entre **agosto e outubro** — "
    "por isso o sistema é ainda mais útil como ferramenta de monitoramento contínuo ao longo do ano."
)

# --- Evolucao no tempo -----------------------------------------------------
st.markdown("### 📈 Evolução dos focos ao longo do tempo")
por_dia = df.groupby(df["data"].dt.date).size().reset_index(name="focos")
por_dia.columns = ["data", "focos"]
fig_tempo = px.bar(
    por_dia,
    x="data",
    y="focos",
    labels={"data": "Data", "focos": "Nº de focos"},
    color="focos",
    color_continuous_scale="YlOrRd",
)
fig_tempo.update_layout(margin=dict(l=0, r=0, t=10, b=0), coloraxis_showscale=False)
st.plotly_chart(fig_tempo, use_container_width=True)

st.divider()

# --- Machine Learning: regioes criticas ------------------------------------
st.markdown("## 🤖 Inteligência Artificial: regiões críticas")
st.markdown(
    "Usamos **clusterização DBSCAN** (aprendizado de máquina não supervisionado) "
    "para agrupar automaticamente os focos que estão próximos uns dos outros. "
    "Assim, em vez de olhar milhares de pontos soltos, a IA aponta as **regiões com "
    "maior concentração de queimadas** — onde o combate deveria ser priorizado."
)

st.sidebar.header("🤖 Parâmetros da IA")
raio_km = st.sidebar.slider("Raio de agrupamento (km)", 2, 30, 10)
min_focos = st.sidebar.slider("Mínimo de focos por região", 3, 30, 8)

df_cl = clusterizar(df, raio_km, min_focos)
n_clusters = df_cl[df_cl["cluster"] != -1]["cluster"].nunique()
n_ruido = int((df_cl["cluster"] == -1).sum())

m1, m2 = st.columns(2)
m1.metric("📍 Regiões críticas identificadas", n_clusters)
m2.metric("• Focos isolados (não agrupados)", f"{n_ruido:,}".replace(",", "."))

if n_clusters == 0:
    st.info("Nenhuma região crítica encontrada com os parâmetros atuais. Tente aumentar o raio ou reduzir o mínimo de focos.")
else:
    # Resumo por cluster: quantos focos, intensidade media e centro geografico.
    resumo = (
        df_cl[df_cl["cluster"] != -1]
        .groupby("cluster")
        .agg(
            focos=("cluster", "size"),
            frp_medio=("frp", "mean"),
            frp_total=("frp", "sum"),
            lat=("latitude", "mean"),
            lon=("longitude", "mean"),
        )
        .reset_index()
    )
    # "Severidade" = quantidade de focos x intensidade media (prioriza regioes
    # que sao grandes E intensas ao mesmo tempo).
    resumo["severidade"] = resumo["focos"] * resumo["frp_medio"]
    resumo = resumo.sort_values("severidade", ascending=False).reset_index(drop=True)
    resumo.insert(0, "ranking", resumo.index + 1)

    st.markdown("#### 🚨 Top regiões mais críticas (priorização para combate)")
    tabela = resumo.head(10).copy()
    tabela = tabela[["ranking", "focos", "frp_medio", "lat", "lon"]]
    tabela.columns = ["Ranking", "Nº de focos", "FRP médio (MW)", "Latitude", "Longitude"]
    st.dataframe(
        tabela.style.format({
            "FRP médio (MW)": "{:.1f}",
            "Latitude": "{:.3f}",
            "Longitude": "{:.3f}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    # Mapa destacando as 10 regioes mais criticas; o restante fica em cinza.
    st.markdown("#### 🗺️ Mapa das 10 regiões mais críticas")
    top_ids = resumo.head(10)["cluster"].tolist()
    rotulos = {cid: f"#{r}" for r, cid in zip(resumo.head(10)["ranking"], top_ids)}

    df_plot = df_cl.copy()
    df_plot["Região"] = df_plot["cluster"].map(rotulos).fillna("Outros focos")
    ordem = [f"#{i}" for i in range(1, 11)] + ["Outros focos"]

    fig_cl = px.scatter_map(
        df_plot,
        lat="latitude",
        lon="longitude",
        color="Região",
        category_orders={"Região": ordem},
        color_discrete_map={"Outros focos": "lightgray"},
        zoom=3.3,
        center={"lat": -5.5, "lon": -60.0},
        map_style="open-street-map",
        height=520,
    )
    fig_cl.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_cl, use_container_width=True)

st.divider()
st.caption(
    "Sentinela Amazônia · POC desenvolvida para a Sub Global Solution 2026.1 (FIAP). "
    "Dados: NASA FIRMS — Fire Information for Resource Management System."
)

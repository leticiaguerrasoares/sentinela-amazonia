"""
download_dados.py
-----------------
Baixa focos de calor (queimadas) detectados por satelite na regiao da
Amazonia Legal usando a API publica do NASA FIRMS (Fire Information for
Resource Management System).

Fonte: satelite VIIRS (instrumento a bordo do Suomi-NPP), que detecta
anomalias termicas na superficie da Terra a partir do espaco.

Como usar:
    1. Pegue uma MAP_KEY gratuita em:
       https://firms.modaps.eosdis.nasa.gov/api/map_key/
    2. Cole a chave no arquivo  config/map_key.txt
       (ou defina a variavel de ambiente FIRMS_MAP_KEY)
    3. Rode:  python scripts/download_dados.py

O resultado e salvo em  data/focos_amazonia.csv
"""

import os
import sys
from pathlib import Path
from datetime import datetime

import requests
import pandas as pd

# --- Configuracoes do recorte ---------------------------------------------

# Caixa delimitadora (bounding box) da Amazonia Legal brasileira.
# Formato exigido pela API: oeste, sul, leste, norte (longitude/latitude).
AREA_AMAZONIA = "-74,-18,-44,5"

# Satelites/produtos VIIRS em tempo quase real (Near Real Time). Combinamos
# os tres para ampliar a cobertura de deteccoes na regiao.
FONTES = ["VIIRS_SNPP_NRT", "VIIRS_NOAA20_NRT", "VIIRS_NOAA21_NRT"]

# Quantidade de dias para tras (a API NRT permite no maximo 5).
DIAS = 5

# Caminhos do projeto (sempre relativos a raiz do projeto, nao ao terminal).
RAIZ = Path(__file__).resolve().parent.parent
ARQ_SAIDA = RAIZ / "data" / "focos_amazonia.csv"
ARQ_CHAVE = RAIZ / "config" / "map_key.txt"


def obter_map_key() -> str:
    """Le a MAP_KEY da variavel de ambiente ou do arquivo config/map_key.txt."""
    chave = os.environ.get("FIRMS_MAP_KEY", "").strip()
    if chave:
        return chave
    if ARQ_CHAVE.exists():
        chave = ARQ_CHAVE.read_text(encoding="utf-8").strip()
        if chave:
            return chave
    print(
        "ERRO: nenhuma MAP_KEY encontrada.\n"
        "  -> Pegue uma chave gratuita em "
        "https://firms.modaps.eosdis.nasa.gov/api/map_key/\n"
        f"  -> Cole a chave dentro do arquivo: {ARQ_CHAVE}"
    )
    sys.exit(1)


def baixar_focos(map_key: str) -> pd.DataFrame:
    """Baixa os focos de cada satelite VIIRS e junta tudo num so DataFrame."""
    from io import StringIO

    partes = []
    for fonte in FONTES:
        url = (
            "https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
            f"{map_key}/{fonte}/{AREA_AMAZONIA}/{DIAS}"
        )
        print(f"Baixando {fonte} (ultimos {DIAS} dias)...")
        resposta = requests.get(url, timeout=60)
        resposta.raise_for_status()

        texto = resposta.text.strip()
        # A API retorna texto de erro (nao CSV) quando algo esta errado.
        if texto.lower().startswith("invalid") or "," not in texto.splitlines()[0]:
            print(f"  AVISO: resposta inesperada para {fonte}: {texto[:120]}")
            continue

        parte = pd.read_csv(StringIO(texto))
        print(f"  -> {len(parte)} focos")
        partes.append(parte)

    if not partes:
        print("ERRO: nenhum dado foi baixado. Verifique a sua MAP_KEY.")
        sys.exit(1)

    return pd.concat(partes, ignore_index=True)


def tratar(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa e organiza as colunas mais importantes para o dashboard."""
    if df.empty:
        print("AVISO: nenhum foco retornado para o periodo/regiao.")
        return df

    # Junta data e hora num unico campo de data/hora.
    df["acq_time"] = df["acq_time"].astype(str).str.zfill(4)
    df["data_hora"] = pd.to_datetime(
        df["acq_date"].astype(str) + " " + df["acq_time"].str[:2] + ":" + df["acq_time"].str[2:],
        errors="coerce",
    )
    df["data"] = pd.to_datetime(df["acq_date"], errors="coerce")

    # frp = Fire Radiative Power (potencia radiativa do fogo, em MW): proxy
    # da intensidade do incendio. Quanto maior, mais intenso o foco.
    df["frp"] = pd.to_numeric(df["frp"], errors="coerce")

    # daynight: D = detectado de dia, N = de noite.
    df["periodo"] = df["daynight"].map({"D": "Dia", "N": "Noite"}).fillna("Desconhecido")

    colunas = [
        "latitude", "longitude", "frp", "confidence",
        "satellite", "data", "data_hora", "periodo",
    ]
    colunas = [c for c in colunas if c in df.columns]
    return df[colunas].dropna(subset=["latitude", "longitude"])


def main() -> None:
    map_key = obter_map_key()
    bruto = baixar_focos(map_key)
    limpo = tratar(bruto)

    ARQ_SAIDA.parent.mkdir(parents=True, exist_ok=True)
    limpo.to_csv(ARQ_SAIDA, index=False)

    print("\n==================== RESUMO ====================")
    print(f"Focos baixados: {len(limpo)}")
    if not limpo.empty:
        print(f"Periodo: {limpo['data'].min().date()} a {limpo['data'].max().date()}")
        print(f"FRP medio: {limpo['frp'].mean():.1f} MW | FRP maximo: {limpo['frp'].max():.1f} MW")
    print(f"Arquivo salvo em: {ARQ_SAIDA}")
    print("===============================================")
    print(f"\nConcluido em {datetime.now():%d/%m/%Y %H:%M}.")


if __name__ == "__main__":
    main()

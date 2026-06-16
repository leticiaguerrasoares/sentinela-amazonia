"""
gerar_diagrama.py
-----------------
Gera a imagem da arquitetura da solucao (assets/arquitetura.png) usada no
README e no relatorio. Desenha um pipeline horizontal de 6 etapas.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrow

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "assets" / "arquitetura.png"

caixas = [
    ("1", "#2563eb", "Satélites VIIRS", ["Detecção de focos de", "calor a partir do espaço", "(Suomi-NPP, NOAA-20/21)"], False),
    ("2", "#0891b2", "API NASA FIRMS", ["Dados abertos de", "queimadas, atualizados", "diariamente"], False),
    ("3", "#16a34a", "Coleta (Python)", ["download_dados.py:", "baixa e limpa os", "dados (Requests)"], False),
    ("4", "#ca8a04", "Base de dados", ["focos_amazonia.csv:", "base estruturada", "(Pandas)"], False),
    ("5", "#ea580c", "Dashboard + IA", ["Streamlit + DBSCAN:", "mapa, indicadores", "e clusterização"], False),
    ("6", "#dc2626", "Priorização", ["Regiões críticas para", "priorizar o combate", "ao fogo"], True),
]

fig, ax = plt.subplots(figsize=(13, 2.7), dpi=160)
ax.set_xlim(0, 1160)
ax.set_ylim(0, 215)
ax.axis("off")

ax.text(16, 200, "Arquitetura da solução — Sentinela Amazônia",
        fontsize=15, fontweight="bold", color="#1a1a1a")

largura, altura = 168, 130
y0 = 30
xs = [16, 208, 400, 592, 784, 976]

for x, (num, cor, titulo, linhas, destaque) in zip(xs, caixas):
    fill = "#fff5f5" if destaque else "#ffffff"
    edge = cor if destaque else "#d0d0d0"
    caixa = FancyBboxPatch(
        (x, y0), largura, altura,
        boxstyle="round,pad=2,rounding_size=10",
        linewidth=1.3, edgecolor=edge, facecolor=fill,
    )
    ax.add_patch(caixa)

    # circulo com o numero da etapa
    ax.add_patch(Circle((x + 24, y0 + altura - 26), 14, color=cor, zorder=3))
    ax.text(x + 24, y0 + altura - 26, num, fontsize=13, fontweight="bold",
            color="white", ha="center", va="center", zorder=4)

    ax.text(x + 44, y0 + altura - 26, titulo, fontsize=12.5, fontweight="bold",
            color="#1a1a1a", ha="left", va="center")

    for i, linha in enumerate(linhas):
        ax.text(x + 14, y0 + altura - 58 - i * 18, linha, fontsize=10, color="#555")

# setas entre as caixas
for i in range(len(xs) - 1):
    x_ini = xs[i] + largura
    ax.add_patch(FancyArrow(x_ini + 2, y0 + altura / 2, 18, 0,
                            width=1.5, head_width=9, head_length=6,
                            length_includes_head=True, color="#888"))

ax.text(16, 12, "Fluxo de dados: do satélite no espaço até a decisão de combate ao fogo na Terra.",
        fontsize=10, color="#999")

plt.tight_layout()
fig.savefig(SAIDA, bbox_inches="tight", facecolor="white")
print(f"Diagrama salvo em: {SAIDA}")

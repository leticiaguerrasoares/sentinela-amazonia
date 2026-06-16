# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%"></a>
</p>

<br>

# 🛰️ Sentinela Amazônia — Monitoramento Inteligente de Queimadas

**Sub Global Solution 2026.1 · Graduação ON em Inteligência Artificial**

## 👩‍🎓 Integrante

- Letícia Angelim Guerra — RM567501

## 👩‍🏫 Professores

### Tutora
- Ana Cristina dos Santos

### Coordenador
- André Godoi Chiovato

## 🎥 Vídeo Demonstrativo

🔗 [Link do vídeo no YouTube (não listado)](INSERIR_LINK_AQUI)

---

## 📜 Descrição

**Sentinela Amazônia** é uma prova de conceito (POC) que aplica Inteligência Artificial e dados de satélite para o **monitoramento de queimadas na Amazônia Legal brasileira**, respondendo à pergunta central da Sub Global Solution 2026.1:

> *Como a Inteligência Artificial e as tecnologias digitais podem transformar a nova economia espacial e gerar impacto positivo na Terra?*

A economia espacial não é feita só de foguetes: **satélites de observação da Terra** geram, todos os dias, enormes volumes de dados que podem salvar florestas e vidas. Este projeto usa exatamente esse tipo de dado — detecções de focos de calor feitas por satélites da NASA — e o transforma em **informação acionável** para o combate ao fogo.

O problema é concreto: a Amazônia sofre com milhares de focos de queimada por dia durante a estação seca. Olhar para milhares de pontos soltos num mapa não ajuda quem precisa decidir **onde agir primeiro**. A solução proposta usa **aprendizado de máquina não supervisionado** para agrupar automaticamente os focos próximos e revelar as **regiões mais críticas**, permitindo priorizar recursos de fiscalização e combate.

### O que a aplicação faz

1. **Coleta dados reais de satélite** — focos de calor detectados pelos satélites VIIRS (NASA FIRMS) nos últimos dias, dentro da caixa geográfica da Amazônia Legal.
2. **Apresenta um dashboard interativo** — mapa dos focos, indicadores (total, intensidade média e máxima), evolução diária e filtros por período, intensidade e horário.
3. **Aplica Inteligência Artificial** — o algoritmo **DBSCAN** agrupa os focos por densidade geográfica e identifica as regiões com maior concentração e intensidade de queimadas, gerando um ranking de prioridade para o combate.

---

## 🛰️ Fonte de Dados

- **NASA FIRMS** (Fire Information for Resource Management System) — API pública e gratuita.
- **Satélites:** VIIRS (Suomi-NPP, NOAA-20 e NOAA-21).
- **Variável principal:** FRP (*Fire Radiative Power*) — a potência radiativa do fogo, em megawatts, usada como medida da intensidade de cada foco.

---

## 🤖 Inteligência Artificial — Como funciona

O coração analítico do projeto é a **clusterização DBSCAN** (*Density-Based Spatial Clustering of Applications with Noise*), um algoritmo de aprendizado de máquina **não supervisionado**:

- Agrupa focos que estão **geograficamente próximos e concentrados**, usando a distância real sobre a esfera terrestre (*haversine*).
- Focos espalhados e isolados são tratados como **ruído**, separando o "sinal" (regiões realmente críticas) do "barulho".
- Cada região identificada recebe um índice de **severidade** = nº de focos × intensidade média (FRP), que ordena o ranking de prioridade.

Diferente de um modelo supervisionado, o DBSCAN **não precisa de dados rotulados** — ele descobre os padrões sozinho, o que é ideal para este problema, em que não temos um "gabarito" das regiões críticas.

---

## 📁 Estrutura de Pastas

```
SUB-GS-Amazonia/
├── assets/                  # imagens (logo da FIAP, diagramas)
├── config/
│   ├── map_key.example.txt  # modelo para a chave da API
│   └── map_key.txt          # sua chave NASA FIRMS (não vai para o Git)
├── data/
│   └── focos_amazonia.csv   # dados baixados do satélite
├── document/
│   └── other/               # documentos de apoio
├── scripts/
│   └── download_dados.py    # baixa os focos da API do NASA FIRMS
├── src/
│   └── app.py               # dashboard Streamlit (aplicação principal)
├── requirements.txt         # dependências Python
└── README.md
```

---

## 🔧 Como Executar

### Pré-requisitos
- Python 3.10 ou superior
- Uma MAP_KEY gratuita do NASA FIRMS

### Passo a passo

1. **Clone o repositório** e entre na pasta do projeto:
   ```bash
   git clone <URL-DO-SEU-REPOSITORIO>
   cd SUB-GS-Amazonia
   ```

2. **Crie o ambiente virtual e instale as dependências:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure a chave da NASA FIRMS:**
   - Pegue uma chave gratuita em: https://firms.modaps.eosdis.nasa.gov/api/map_key/
   - Crie o arquivo `config/map_key.txt` e cole **somente a chave** dentro dele.

4. **Baixe os dados de satélite:**
   ```bash
   python scripts/download_dados.py
   ```

5. **Inicie o dashboard:**
   ```bash
   streamlit run src/app.py
   ```
   O aplicativo abre automaticamente no navegador em `http://localhost:8501`.

---

## 📊 Resultados

Com os dados reais de 5 dias de observação na Amazônia Legal, a aplicação:

- Processou **mais de 10.000 focos de calor** detectados por satélite.
- Identificou automaticamente as **regiões críticas** (clusters densos) e as ordenou por severidade.
- Apresentou tudo em um dashboard interativo, com mapa, indicadores e priorização — pronto para apoiar a tomada de decisão no combate a incêndios.

> Os números variam a cada execução, pois os dados são atualizados diariamente pelos satélites.

---

## ⚠️ Limitações e Próximos Passos

- **Janela temporal curta:** a API em tempo quase real fornece no máximo 5 dias de histórico. Para análises sazonais, seria necessário o arquivo histórico do FIRMS.
- **Foco de calor ≠ queimada confirmada:** o satélite detecta anomalias térmicas, que na maioria são queimadas, mas podem incluir outras fontes de calor.
- **Próximos passos:** integrar dados climáticos para **prever** risco de fogo, adicionar séries históricas e publicar a aplicação na nuvem (ex.: Streamlit Cloud ou AWS).

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Streamlit** — dashboard interativo
- **Pandas / NumPy** — manipulação de dados
- **scikit-learn** — clusterização DBSCAN
- **Plotly** — mapas e gráficos interativos
- **Requests** — consumo da API do NASA FIRMS

---

## 📋 Licença

Este projeto acadêmico segue o modelo de documentação FIAP.

MODELO GIT FIAP por FIAP está licenciado sob Attribution 4.0 International.

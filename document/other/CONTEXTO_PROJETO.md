# CONTEXTO DO PROJETO — para retomar em nova conversa

> **Como usar:** em uma conversa nova com o Claude, diga:
> *"Leia o arquivo `SUB-GS-Amazonia/document/other/CONTEXTO_PROJETO.md` e continue de onde paramos."*

---

## Quem / qual entrega
- **Aluna:** Letícia Angelim Guerra — **RM567501** (atividade **INDIVIDUAL**)
- **Entrega:** Sub Global Solution 2026.1 (FIAP) — tema: economia espacial + IA com impacto na Terra
- **Prazo:** até a noite de ~16/06/2026 (CONFERIR na plataforma)
- ⚠️ É individual: a solução tem que ser distinta da de colegas (risco de plágio).

## O que é o projeto
**Sentinela Amazônia** — dashboard que monitora **queimadas na Amazônia Legal** usando
**dados reais de satélite (NASA FIRMS / VIIRS)** e **IA (clusterização DBSCAN)** para
apontar as regiões mais críticas (priorização de combate).

## Onde está / como rodar
- Pasta: `/Users/leticiaguerra/untitled folder/SUB-GS-Amazonia`
- Ambiente Python já criado em `.venv` (streamlit, pandas, scikit-learn, plotly, requests, numpy, matplotlib)
- Rodar o app: `.venv/bin/streamlit run src/app.py` → http://localhost:8501
- Rebaixar dados: `.venv/bin/python scripts/download_dados.py` (usa a chave em `config/map_key.txt`)
- Chave NASA FIRMS já salva em `config/map_key.txt` (NÃO subir no GitHub)

## Status — JÁ FEITO ✅
- `src/app.py` — dashboard (mapa, indicadores, gráfico, filtros, seção de IA DBSCAN com Top 10)
- `scripts/download_dados.py` — baixa focos de 3 satélites VIIRS (5 dias, box Amazônia Legal)
- `data/focos_amazonia.csv` — 10.531 focos REAIS (período 11–15/06/2026)
- `README.md` — completo
- `assets/arquitetura.png` e `.svg` — diagrama da solução
- `scripts/gerar_diagrama.py` — gera o diagrama
- `document/RELATORIO.md` — texto-base do PDF
- `document/ROTEIRO_VIDEO.md` — roteiro do vídeo (5 min)
- `document/Relatorio_Sentinela_Amazonia.docx` — Word pronto (diagrama embutido + 4 espaços marcados pros prints + 2 links a preencher)

## Status — FALTA ⏳
1. **GitHub** — subir o projeto (git init/commit/push). Repo público sugerido: `sentinela-amazonia`.
   Usuário GitHub da aluna: `leticiaguerrasoares`. NÃO commitar `.venv/` nem `config/map_key.txt` (já no `.gitignore`).
2. **Vídeo** — gravar seguindo o roteiro, subir no YouTube **"Não listado"**, pegar o link.
3. **PDF** — abrir o `.docx`, colar os 4 prints, preencher os 2 links (repo + vídeo), exportar PDF.
4. **Entrega** — subir o PDF na plataforma da FIAP (com os links dentro).

## Decisões técnicas (para explicar no vídeo/PDF)
- Recorte **Amazônia Legal** (box `-74,-18,-44,5`): inclui o "arco do desmatamento".
- **3 satélites VIIRS** (SNPP, NOAA-20, NOAA-21) para mais cobertura; API permite no máx. 5 dias.
- **DBSCAN** (não supervisionado) com distância **haversine**, `eps = raio_km / 6371`.
- **Severidade = nº de focos × FRP médio** (prioriza regiões grandes E intensas).
- **Sazonalidade:** em junho o fogo se concentra no sul/leste (arco do desmatamento + Cerrado);
  pico na floresta é entre **agosto e outubro**. (Isso é um argumento forte, não um bug.)

## Prints já tirados (a aluna tem)
1. Painel principal (título + indicadores + mapa)
2. Nota de sazonalidade + gráfico de evolução
3. Seção de IA (regiões críticas + tabela Top 10)
4. Mapa das 10 regiões mais críticas

# Roteiro do Vídeo — Sentinela Amazônia (até 5 min)

> Dica: NÃO leia palavra por palavra (fica com cara de robô/IA). Use os tópicos
> como guia e fale com naturalidade, do seu jeito. Grave a tela do dashboard
> rodando enquanto explica. Lembre: vídeo **"Não Listado"** no YouTube.

---

## ⏱️ 0:00 – 0:30 | Abertura
- "Oi, eu sou a Letícia Angelim Guerra, RM 567501."
- "Esse é o meu projeto pra Sub Global Solution 2026.1: o **Sentinela Amazônia**."
- "A pergunta do desafio era: como a IA e as tecnologias da economia espacial podem gerar impacto positivo na Terra. A minha resposta foca em **queimadas na Amazônia**."

## ⏱️ 0:30 – 1:15 | O problema
- "Satélites no espaço detectam focos de calor na Terra todos os dias — isso é economia espacial gerando dado útil."
- "O problema não é só saber que tem fogo. É que são **milhares de pontos** num mapa, e alguém precisa decidir **onde agir primeiro**."
- "Meu projeto usa esses dados de satélite + Inteligência Artificial pra responder isso automaticamente."

## ⏱️ 1:15 – 2:00 | A solução (mostrar o diagrama de arquitetura)
- Mostre a imagem `assets/arquitetura.svg`.
- "O fluxo é: o satélite VIIRS detecta o fogo → a API da NASA disponibiliza o dado → meu script em Python baixa e limpa → vira uma base de dados → e o dashboard mostra tudo e aplica a IA."

## ⏱️ 2:00 – 3:15 | Demonstração do dashboard (tela ao vivo)
- Abra o app em http://localhost:8501.
- "Aqui em cima tenho os indicadores: mais de 10 mil focos reais nos últimos 5 dias, a intensidade média e a máxima."
- Mostre o **mapa**: "cada ponto é um foco; a cor e o tamanho mostram a intensidade do fogo, o FRP."
- Mexa em um **filtro** (ex.: intensidade mínima) pra mostrar que é interativo.
- **Ponto forte (mostra que você entende):** "Repara que o fogo está concentrado no sul e leste, não no meio da floresta. Isso é a estação seca começando — em junho o fogo fica no arco do desmatamento; o pico na floresta é entre agosto e outubro."

## ⏱️ 3:15 – 4:30 | A Inteligência Artificial
- Desça até a seção "🤖 Inteligência Artificial: regiões críticas".
- "Aqui entra o Machine Learning. Eu uso um algoritmo chamado **DBSCAN**, que é uma clusterização não supervisionada."
- "Ele agrupa automaticamente os focos que estão próximos e concentrados, e ignora os pontos isolados."
- Mostre a **tabela do Top 10** e o **mapa colorido**: "essas são as regiões mais críticas, ranqueadas por severidade — quantidade de focos vezes a intensidade média. É isso que diria pra uma brigada onde ir primeiro."
- Mexa nos sliders de raio/mínimo de focos pra mostrar que a IA é ajustável.

## ⏱️ 4:30 – 5:00 | Conclusão
- "Então, em resumo: dados que vêm do espaço viram uma ferramenta concreta de combate ao fogo aqui na Terra."
- "Como próximos passos, dá pra integrar dados de clima pra **prever** o risco de queimada, e publicar isso na nuvem."
- "Obrigada!"

---

### ✅ Checklist antes de gravar
- [ ] Dashboard aberto e funcionando (http://localhost:8501)
- [ ] Diagrama de arquitetura aberto pra mostrar
- [ ] Áudio limpo, sem barulho
- [ ] Duração final **até 5 minutos**
- [ ] Subir no YouTube como **"Não Listado"** e copiar o link

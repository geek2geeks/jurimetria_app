# Relatório de Ética e Privacidade

O projeto JurisTriage opera sob uma camada estrita de ética, tratando dados que, embora pertençam aos domínios da Jurisprudência Pública e abertamente disponíveis nos Diários da República e Portais de Transparência de Portugal (IGFEJ), impõem riscos claros em escala de Extração em Massa de Dados (Scraping/NLP).

## O Desafio e as Restrições (RGPD)
- O texto judicial português é rico e raramente totalmente anonimizado. Existem recorrentemente nomes de arguidos que, isoladamente em processos abertos, não chocam com a lei, mas quando arrastados para bases de dados compiladas de grandes proporções e pesquisáveis (Big Data), roçam o conflito com as balizas da nova regulamentação de proteção do RGPD Europeu.
- **Portanto:** É proibido colocar o corpus bruto ou JSONs com dados pessoais no GitHub ou em serviços externos de IA. Apenas amostras sintéticas ou sanitizadas podem ser partilhadas. Matrizes TF-IDF reduzem a legibilidade direta, mas não são encriptação nem anonimização. Vocabulários e artefactos também podem conter informação identificável.

## Preconceito e a Ética Algorítmica (Algorithmic Bias)
Qualquer Classificador Neural de "Rótulos Judiciais" vai descobrir, na natureza das coisas, atalhos estatísticos terríveis:
- A equipa de vetorização e limpeza deve avaliar stop-words e `min_df`. O `min_df` pode reduzir termos raros, incluindo alguns nomes próprios, mas não garante remoção de dados pessoais nem elimina viés. São necessárias amostras sanitizadas, testes e análise crítica dos erros.

## Uso de IA externa

- Não enviar PDFs, JSONs reais, `full_text`, `decisao_raw`, dados pessoais ou artefactos identificáveis para OpenCode, DeepSeek ou outro fornecedor.
- Não incluir segredos em prompts, screenshots ou logs.
- Usar apenas exemplos sintéticos ou sanitizados.
- Identificar claramente qualquer texto produzido por LLM.

## Requisitos de Publicação de Pesquisa
Toda e qualquer tabela de exemplos criada pela equipa para efeitos de demonstrações em slides ou nos tutoriais de `README.md` têm de estar sanitizadas (e.g. O nome "José Silvério" vira "[Autor 1]"). Nenhuma apresentação de avaliação do semestre pode comprometer o repouso identitário real do processo referenciado.

# Visão e missão do projeto

O **JurisTriage PT** não pretende ser a "solução definitiva" que vai substituir juízes ou advogados em Portugal. Trata-se de uma Prova de Conceito Académica (PoC).

## Declaração Ética
O processamento automático de jurisprudência traz sérias preocupações éticas que queremos mitigar ativamente:
1. **Bias (Viés):** Algoritmos estatísticos tendem a repetir os preconceitos do passado.
2. **Transparência:** Modelos MLP não oferecem, por si só, uma fundamentação jurídica. O módulo opcional de LLM pode formatar uma descrição legível do resultado, mas esse texto é gerado, pode conter erros e não transforma o classificador num sistema explicável.
3. **Anonimização e RGPD:** O uso de TF-IDF com limites como `min_df` pode reduzir a presença de termos raros, incluindo alguns nomes próprios, mas não garante anonimização formal. Por isso, as pastas de dados originais ficam fora da submissão final do Git e qualquer exemplo público deve ser sanitizado.

## Lema da Equipa
*"O objetivo não é construir o modelo jurídico mais sofisticado possível. O objetivo é demonstrar engenharia de software aplicada a IA: dados limpos, código modular, tipagem estrita, testes rigorosos e colaboração humana inteligente."*

# Relatório estrutural da inspeção do corpus PDF

Este relatório reúne os resultados empíricos da inspeção de uma amostra do corpus do CSM (Conselho Superior da Magistratura de Portugal), para garantir que as especificações do analisador assentam em evidência e não apenas em pressupostos.

## 1. Conclusão da inspeção
A pequena amostra inspecionada sugere estabilidade do formato em bruto, mas não permite estimar a conformidade do corpus completo. Os valores e nomes dos campos variam, pelo que o analisador deve ser tolerante.

- **Variação temporal:** A amostra contém documentos de diferentes tribunais e anos. Nela, a tabela de metadados aparece com estrutura semelhante, mas esta observação não constitui garantia para todo o corpus.
- **Exceções Identificadas Praticamente:** O formato que diz `"Data do Acórdão"` tem oscilações de nomenclatura temporal por variação de escrivães nos tribunais periféricos. A área delimitadora "Decisão Integral:" raramente surge explícita nas sentenças sumarizadas ou de menor impacto, e "III - Decisão" não aparece nativamente nos documentos curtos (<3 páginas) de recurso simples, uma vez que toda a decisão é resolvida em dois parágrafos fundidos.
- **Diagnóstico do analisador:** campos ausentes ou formatos inesperados devem produzir `None` e um registo de erro, sem interromper o lote. A inspeção atual não sustenta percentagens para a frequência dessas exceções. O controlo de memória deve ser tratado separadamente através de iteradores e limites de processamento.

## 2. Evidência dos dados em bruto
Baseado no varrimento mecânico de extração textual com pdfplumber em `inspecionar_pdfs.py`:

| Ficheiro PDF Extrato | Tribunal Origem | Data Assumida | Quantidade Págs | Presença do URL & ECLI Base | Presença Pág.1: Relator / Tabela C2 / Sumário | Layout Típico "Decisão Integral" / "III" Final | Presença de Footer PDF Limpável? |
|---|---|---|---|---|---|---|---|
| ECLI_PT_STA_1950_000565.1D.pdf | STA | 1950 | 2 | VERIFICADO | VERIFICADO | FALHOU/OMISSO | VERIFICADO |
| ECLI_PT_TRG_2002_1142.02.2.50.pdf | TRG | 2002 | 2 | VERIFICADO | VERIFICADO | VERIFICADO | VERIFICADO |
| ECLI_PT_STA_1972_002024.68.pdf | STA | 1972 | 2 | VERIFICADO | VERIFICADO | FALHOU/OMISSO | VERIFICADO |
| ECLI_PT_TRP_1976_0012904.3E.pdf | TRP | 1976 | 2 | VERIFICADO | VERIFICADO | FALHOU/OMISSO | VERIFICADO |
| ECLI_PT_TRE_1998_1372.97.3.2C.pdf | TRE | 1998 | 4 | VERIFICADO | VERIFICADO | VERIFICADO | VERIFICADO |
| ECLI_PT_STJ_1936_024074.54.pdf | STJ | 1936 | 4 | VERIFICADO | VERIFICADO | HÍBRIDO | VERIFICADO |
| ECLI_PT_TRC_1999_105.99.6B.pdf | TRC | 1999 | 2 | VERIFICADO | VERIFICADO | VERIFICADO | VERIFICADO |
| ECLI_PT_TRL_1976_0012080.79.pdf | TRL | 1976 | 2 | VERIFICADO | VERIFICADO | FALHOU/OMISSO | VERIFICADO |

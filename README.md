# JudgeBlender-Implementation
Este repositório contém uma implementação independente do framework JudgeBlender, baseada no artigo "JudgeBlender: Ensembling Automatic Relevance Judgments" (Rahmani et al., 2025). O objetivo é automatizar julgamentos de relevância em Information Retrieval (IR) utilizando ensemblagem de modelos de linguagem (LLMs) open-source para mitigar vieses de modelos únicos.

## Arquitetura do Projeto

De acordo com a metodologia detalhada na Seção 3 do artigo, o framework foi estruturado de forma modular para suportar duas variantes principais:
- PromptBlender (Single Model, Multi-Prompt): Conforme descrito no setup experimental, utiliza o modelo Meta-Llama-3-8B para explorar três "vias de raciocínio" distintas através de diferentes estratégias de prompting: Thomas et al., MultiCriteria (Farzi) e o método Two-step de Sun et al.
- LLMBlender (Multi-Model, Multi-Prompt): Conforme a Tabela 2 e a Seção 4, utiliza um painel diversificado composto por modelos de diferentes famílias (Mistral-7B, Gemma-7B e Llama-3-8B) para capturar forças complementares e reduzir o viés intrínseco de cada arquitetura.
- Aggregator: Implementação das funções de agregação por média (AV) e maioria (MV). Para o método de votação por maioria, incluí as quatro estratégias de desempate especificadas pelos autores: Random (Rnd), Maximum (Max), Minimum (Min) e Average (Avg).

## Estrutura de Arquivos

- `src/utils/injector.py`: Biblioteca interna para formatação e injeção de dados em prompts multi-estágio.
- `src/prompt_blender/`: Orquestração de inferência para via única de modelo.
- `src/aggregator/`: Processamento de consenso e cálculo de scores finais.
- `prompts/`: Templates de prompts baseados na engenharia reversa das descrições contidas nas seções 3 e 4 do artigo.

## Status Atual

- [x] Modelagem da infraestrutura de injeção.
- [x] Orquestrador do PromptBlender funcional.
- [ ] Finalização da coleta de resultados (inferência via Google Colab).
- [ ] Análise de correlação (Cohen's Kappa e NDCG@10) com os labels humanos do TREC DL 2023.

## Reference
```bib
@misc{rahmani2024judgeblenderensemblingjudgmentsautomatic,
      title={JudgeBlender: Ensembling Judgments for Automatic Relevance Assessment}, 
      author={Hossein A. Rahmani and Emine Yilmaz and Nick Craswell and Bhaskar Mitra},
      year={2024},
      eprint={2412.13268},
      archivePrefix={arXiv},
      primaryClass={cs.IR},
      url={https://arxiv.org/abs/2412.13268}, 
}
```

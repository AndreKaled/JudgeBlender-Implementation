import ir_datasets

# Carregando o dataset oficial do TREC DL 2023 usado no artigo
dataset = ir_datasets.load("msmarco-passage/trec-dl-2023")

# vendo as Queries
print("Exemplo de Query:")
for query in dataset.queries_iter()[:1]:
    print(f"ID: {query.query_id} | Texto: {query.text}")

# vendo os Qrels (Julgamentos humanos)
print("\nExemplo de Qrel (Label):")
for qrel in dataset.qrels_iter()[:1]:
    print(f"Query ID: {qrel.query_id} | Doc ID: {qrel.doc_id} | Score: {qrel.relevance}")
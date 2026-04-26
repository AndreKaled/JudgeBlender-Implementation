import json

def probe_files():
    print("--- Probing Queries ---")
    with open("data/llm4eval_query_2024.txt", "r") as f:
        print(f"Linha 1: {f.readline().strip()}")

    print("\n--- Probing Documents (JSONL) ---")
    with open("data/llm4eval_document_2024.jsonl", "r") as f:
        first_line = json.loads(f.readline())
        print(f"Chaves disponíveis: {list(first_line.keys())}")
        print(f"Conteúdo: {str(first_line)[:200]}...")

    print("\n--- Probing Qrels ---")
    with open("data/llm4eval_test_qrel_2024.txt", "r") as f:
        print(f"Linha 1: {f.readline().strip()}")

probe_files()
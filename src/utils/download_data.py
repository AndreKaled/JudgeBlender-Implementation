import os

# Download via git
os.system("git clone https://github.com/llm4eval/LLMJudge.git temp_data")

# move tudo de data/ para a raiz e apaga o resto
os.system("mkdir -p data && mv temp_data/data/* data/ && rm -rf temp_data")

print("Arquivos na pasta data:", os.listdir("data"))
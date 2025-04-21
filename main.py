import os
from datetime import datetime, timedelta
import random

total_commits = 200  # pode aumentar depois

print("Iniciando...")

for i in range(total_commits):
    # dias aleatórios no passado
    days_ago = random.randint(0, 365)
    random_date = datetime.now() - timedelta(days=days_ago)

    date_str = random_date.strftime("%Y-%m-%d %H:%M:%S")

    with open("data.txt", "a", encoding="utf-8") as f:
        f.write(f"Commit {i} - {date_str}\n")

    os.system("git add .")

    # 🔥 IMPORTANTE: define data fake
    os.system(f'git commit --date="{date_str}" -m "commit {i}"')

print("Enviando...")
os.system("git push")

print("Finalizado!")
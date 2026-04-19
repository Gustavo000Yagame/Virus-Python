import os
from datetime import datetime

for i in range(10):
    with open("data.txt", "a") as f:
        f.write(f"Commit {i} - {datetime.now()}\n")

    os.system("git add .")
    os.system(f'git commit -m "commit {i}"')

os.system("git push")
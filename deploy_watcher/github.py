import requests
from datetime import datetime, timedelta
from rich import print

def check_github(config):
    token = config.get("token")
    repos = config.get("repos", [])
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    alerts = []

    for repo in repos:
        owner, name = repo.split("/")
        url = f"https://api.github.com/repos/{owner}/{name}/pulls"
        r = requests.get(url, headers=headers)

        if r.status_code != 200:
            print(f"[red]Erro ao acessar {repo}: {r.status_code}[/red]")
            continue

        for pr in r.json():
            updated_at = datetime.strptime(pr["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
            if datetime.utcnow() - updated_at > timedelta(days=3):
                alerts.append(f"⚠️ PR parado há mais de 3 dias em {repo}: {pr['title']}")

    return alerts
import requests
from datetime import datetime, timedelta
from rich import print

def check_gitlab(config):
    token = config.get("token")
    projects = config.get("projects", [])
    headers = {
        "PRIVATE-TOKEN": token
    }

    alerts = []

    for project_id in projects:
        url = f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests?state=opened"
        r = requests.get(url, headers=headers)

        if r.status_code != 200:
            print(f"[red]Erro ao acessar projeto {project_id}: {r.status_code}[/red]")
            continue

        for mr in r.json():
            updated_at = datetime.strptime(mr["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            if datetime.utcnow() - updated_at > timedelta(days=3):
                alerts.append(f"⚠️ MR parado há mais de 3 dias no projeto {project_id}: {mr['title']}")

    return alerts

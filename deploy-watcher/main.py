import sys
import os
import time
from rich import print

# Usa o diretório de trabalho atual como base
base_dir = os.getcwd()
sys.path.insert(0, os.path.join(base_dir, 'watcher'))
sys.path.insert(0, os.path.join(base_dir, 'utils'))

from github import check_github
from gitlab import check_gitlab
from notifier import send_alerts
from config import load_config

def main():
    print("[bold cyan]\U0001F680 Deploy Watcher iniciado...[/bold cyan]")
    config = load_config()
    interval = config.get("interval", 300)

    while True:
        print("[yellow]\U0001F50D Verificando repositórios...[/yellow]")

        github_alerts = check_github(config.get("github", {}))
        gitlab_alerts = check_gitlab(config.get("gitlab", {}))

        all_alerts = github_alerts + gitlab_alerts
        if all_alerts:
            send_alerts(all_alerts, config["notifications"])
        else:
            print("[green]Nenhum alerta encontrado.[/green]")

        if config.get("one_shot", False):
            break

        print(f"[blue]⏲️ Aguardando {interval} segundos...[/blue]")
        time.sleep(interval)


if __name__ == "__main__":
    main()
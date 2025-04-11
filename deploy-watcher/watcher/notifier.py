import requests
import smtplib
from email.message import EmailMessage
from rich import print

def send_alerts(alerts, config):
    if config.get("slack"):
        send_to_slack(alerts, config["slack"])

    if config.get("discord"):
        send_to_discord(alerts, config["discord"])

    if config.get("email"):
        send_email(alerts, config["email"])

def send_to_slack(alerts, slack_config):
    webhook = slack_config["webhook"]
    msg = "\n".join(alerts)
    requests.post(webhook, json={"text": msg})
    print("[blue]Notificações enviadas ao Slack[/blue]")

def send_to_discord(alerts, discord_config):
    webhook = discord_config["webhook"]
    msg = "\n".join(alerts)
    requests.post(webhook, json={"content": msg})
    print("[magenta]Notificações enviadas ao Discord[/magenta]")

def send_email(alerts, email_config):
    msg = EmailMessage()
    msg.set_content("\n".join(alerts))
    msg["Subject"] = "Deploy Watcher - Alertas"
    msg["From"] = email_config["from"]
    msg["To"] = email_config["to"]

    with smtplib.SMTP_SSL(email_config["smtp_server"], email_config["port"]) as smtp:
        smtp.login(email_config["from"], email_config["password"])
        smtp.send_message(msg)
    print("[green]Email enviado com sucesso[/green]")

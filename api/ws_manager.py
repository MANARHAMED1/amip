import asyncio
import json
import smtplib
import os
from email.mime.text import MIMEText
from collections import defaultdict
from fastapi import WebSocket

SMTP_HOST = os.getenv("SMTP_HOST", "mailhog")
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
SMTP_FROM = os.getenv("SMTP_FROM", "amip@amm.local")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "admin@amm.local")
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")


class ConnectionManager:
    def __init__(self):
        self._connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self._connections.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self._connections:
            self._connections.remove(ws)

    async def broadcast(self, message: dict):
        msg = json.dumps(message, default=str)
        stale = []
        for ws in self._connections:
            try:
                await ws.send_text(msg)
            except Exception:
                stale.append(ws)
        for ws in stale:
            self.disconnect(ws)

    @property
    def count(self) -> int:
        return len(self._connections)


manager = ConnectionManager()


def send_email_alert(subject: str, body: str):
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = SMTP_FROM
        msg["To"] = NOTIFY_EMAIL
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=5) as s:
            if SMTP_USER and SMTP_PASSWORD:
                s.starttls()
                s.login(SMTP_USER, SMTP_PASSWORD)
            s.sendmail(SMTP_FROM, [NOTIFY_EMAIL], msg.as_string())
    except Exception:
        pass


async def check_alerts_background():
    from api.database import fetch_all
    known_broken: set[str] = set()
    while True:
        try:
            machines = fetch_all("SELECT code, nom, statut FROM machine ORDER BY code")
            broken = {m["code"] for m in machines if m["statut"] == "BROKEN"}
            new_broken = broken - known_broken
            fixed = known_broken - broken
            now_str = __import__("datetime").datetime.now().isoformat()
            for code in new_broken:
                m = next((x for x in machines if x["code"] == code), {})
                msg = {
                    "type": "machine_down",
                    "machine_code": code,
                    "machine_name": m.get("nom", code),
                    "timestamp": now_str,
                    "message": f"Machine {code} ({m.get('nom', '')}) est en panne!",
                }
                await manager.broadcast(msg)
                send_email_alert(
                    f"[AMIP] Panne machine {code}",
                    f"Machine: {m.get('nom', code)}\nCode: {code}\nDate: {now_str}\n\nCette machine est en panne. Intervention requise.",
                )
            for code in fixed:
                msg = {
                    "type": "machine_restored",
                    "machine_code": code,
                    "timestamp": now_str,
                    "message": f"Machine {code} est de nouveau operationnelle.",
                }
                await manager.broadcast(msg)
            known_broken = broken
            # also check maintenance due soon
            due = fetch_all("""
                SELECT ma.code, ma.nom, m.date_intervention, m.type_intervention
                FROM maintenance m
                JOIN machine ma ON m.machine_id = ma.machine_id
                WHERE ma.statut != 'BROKEN'
                  AND m.date_intervention BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '3 days'
                ORDER BY m.date_intervention
            """)
            for d in due:
                msg = {
                    "type": "maintenance_due",
                    "machine_code": d["code"],
                    "machine_name": d["nom"],
                    "date": str(d["date_intervention"]),
                    "type": d["type_intervention"],
                    "timestamp": now_str,
                    "message": f"Maintenance {d['type_intervention']} pour {d['code']} prevue le {d['date_intervention']}.",
                }
                await manager.broadcast(msg)
        except Exception:
            pass
        await asyncio.sleep(30)

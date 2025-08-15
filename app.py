from flask import Flask, Response
import requests
import os
from datetime import datetime

app = Flask(__name__)

API_KEY = os.getenv("API_FOOTBALL_KEY", "35ef30ccdeca895feefc8a0d80e3921d")

# IDs das ligas na API-Football
LIGAS_BR = {
    71: "Brasileirão Série A",
    73: "Copa do Brasil"
}

@app.route("/jogos-hoje-whatsapp")
def jogos_hoje_whatsapp():
    hoje_formatado = datetime.now().strftime("%d/%m/%Y")
    hoje_api = datetime.now().strftime("%Y-%m-%d")

    texto = f"*OS PRINCIPAIS JOGOS*⚽\n*DE HOJE ({hoje_formatado})*\n\n"

    for liga_id, nome_liga in LIGAS_BR.items():
        url = f"https://v3.football.api-sports.io/fixtures?date={hoje_api}&league={liga_id}&season=2025"
        headers = {"x-apisports-key": API_KEY}
        resp = requests.get(url, headers=headers)
        dados = resp.json()

        if not dados.get("response"):
            continue

        for jogo in dados["response"]:
            time1 = jogo["teams"]["home"]["name"]
            time2 = jogo["teams"]["away"]["name"]
            hora = datetime.fromisoformat(jogo["fixture"]["date"][:-1]).strftime("%H:%M")
            canal = ", ".join(jogo["fixture"].get("tv", []) or []) or "Não informado"
            campeonato = jogo["league"]["name"]

            texto += f"🇧🇷 {time1} x {time2}\n🕒 {hora}\n📺 {canal}\n🌐 {campeonato}\n\n"

        texto += "\n"

    return Response(texto.strip(), mimetype="text/plain; charset=utf-8")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

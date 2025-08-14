from flask import Flask, jsonify, Response
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Sua chave gratuita da API-Football
API_KEY = os.getenv("API_FOOTBALL_KEY", "SUA_CHAVE_AQUI")

# ID da liga - Brasileirão Série A
LEAGUE_ID = 71

@app.route("/jogos-hoje")
def jogos_hoje():
    hoje = datetime.now().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}&league={LEAGUE_ID}&season=2025"
    headers = {"x-apisports-key": API_KEY}
    resp = requests.get(url, headers=headers)
    dados = resp.json()
    return jsonify(dados)

@app.route("/jogos-hoje-whatsapp")
def jogos_hoje_whatsapp():
    hoje_formatado = datetime.now().strftime("%d/%m/%Y")
    hoje_api = datetime.now().strftime("%Y-%m-%d")

    url = f"https://v3.football.api-sports.io/fixtures?date={hoje_api}&league={LEAGUE_ID}&season=2025"
    headers = {"x-apisports-key": API_KEY}
    resp = requests.get(url, headers=headers)
    dados = resp.json()

    texto = f"*OS PRINCIPAIS JOGOS*⚽\n*DE HOJE ({hoje_formatado})*\n\n"

    for jogo in dados.get("response", []):
        time1 = jogo["teams"]["home"]["name"]
        time2 = jogo["teams"]["away"]["name"]
        hora = datetime.fromisoformat(jogo["fixture"]["date"][:-1]).strftime("%H:%M")
        canal = ", ".join(jogo["fixture"].get("tv", []) or []) or "Não informado"
        campeonato = jogo["league"]["name"]

        texto += f"🇧🇷 {time1} x {time2}\n🕒 {hora}\n📺 {canal}\n🌐 {campeonato}\n\n"

    return Response(texto, mimetype="text/plain; charset=utf-8")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

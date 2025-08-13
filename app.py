from flask import Flask, jsonify, Response
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Sua chave gratuita da API-Football (substitua aqui)
API_KEY = os.getenv("API_FOOTBALL_KEY", "SUA_CHAVE_AQUI")

@app.route("/jogos-hoje")
def jogos_hoje():
    hoje = datetime.now().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}&country=Brazil"
    headers = {"x-apisports-key": API_KEY}
    resp = requests.get(url, headers=headers)
    dados = resp.json()
    return jsonify(dados)

@app.route("/jogos-hoje-whatsapp")
def jogos_hoje_whatsapp():
    hoje = datetime.now().strftime("%d/%m/%Y")
    url = f"https://v3.football.api-sports.io/fixtures?date={datetime.now().strftime('%Y-%m-%d')}&country=Brazil"
    headers = {"x-apisports-key": API_KEY}
    resp = requests.get(url, headers=headers)
    dados = resp.json()

    texto = f"*OS PRINCIPAIS JOGOS*⚽\n*DE HOJE ({hoje})*\n\n"
    for jogo in dados.get("response", []):
        time1 = jogo["teams"]["home"]["name"]
        time2 = jogo["teams"]["away"]["name"]
        hora = datetime.fromisoformat(jogo["fixture"]["date"][:-1]).strftime("%H:%M")
        canal = ", ".join(tv for tv in jogo["fixture"].get("tv", []) if tv) or "Não informado"
        campeonato = jogo["league"]["name"]
        texto += f"🇧🇷 {time1} x {time2}\n🕒 {hora}\n📺 {canal}\n🌐 {campeonato}\n\n"

    return Response(texto, mimetype="text/plain; charset=utf-8")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

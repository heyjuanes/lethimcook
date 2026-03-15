# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
import psycopg2
import os
import requests
import json
import re

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "recetas"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres123")
    )

def init_db():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS recetas (
                id SERIAL PRIMARY KEY,
                ingredientes TEXT NOT NULL,
                receta TEXT NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error DB: {e}")

def generar_receta(ingredientes):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "Eres un chef profesional. Responde SIEMPRE en este formato JSON exacto sin markdown ni texto adicional: {\"nombre\": \"Nombre del plato\", \"tiempo\": \"X minutos\", \"porciones\": \"X porciones\", \"dificultad\": \"Facil/Medio/Dificil\", \"imagen_keyword\": \"keyword en ingles\", \"ingredientes\": [\"ingrediente con cantidad\"], \"pasos\": [{\"titulo\": \"Titulo corto\", \"detalle\": \"Explicacion detallada\"}], \"consejo\": \"Consejo del chef\"}"
            },
            {
                "role": "user",
                "content": f"Ingredientes disponibles: {ingredientes}. Crea una receta deliciosa y detallada."
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.8
    }
    response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
    data = response.json()
    content = data["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        content = re.sub(r"```json|```", "", content).strip()
    return json.loads(content)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generar", methods=["POST"])
def generar():
    data = request.get_json()
    ingredientes = data.get("ingredientes", "")
    if not ingredientes:
        return jsonify({"error": "No se recibieron ingredientes"}), 400
    try:
        receta = generar_receta(ingredientes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO recetas (ingredientes, receta) VALUES (%s, %s)",
                    (ingredientes, json.dumps(receta, ensure_ascii=False)))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error DB: {e}")
    return jsonify({"receta": receta})

@app.route("/historial")
def historial():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, ingredientes, receta, fecha FROM recetas ORDER BY fecha DESC LIMIT 10")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        result = []
        for r in rows:
            try:
                receta_data = json.loads(r[2])
                nombre = receta_data.get("nombre", "Receta")
            except:
                nombre = "Receta"
                receta_data = {}
            result.append({
                "id": r[0],
                "ingredientes": r[1],
                "receta_nombre": nombre,
                "receta_json": json.dumps(receta_data, ensure_ascii=False),
                "fecha": str(r[3])
            })
        return jsonify(result)
    except:
        return jsonify([])

@app.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar(id):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM recetas WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/eliminar-todo", methods=["DELETE"])
def eliminar_todo():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM recetas")
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)
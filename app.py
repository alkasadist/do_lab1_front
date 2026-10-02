import os

import requests
from flask import Flask, render_template_string, request

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

app = Flask(__name__)

PAGE = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>Frontend v2.0</title></head>
<body>
  <form method="post" action="/send">
    <input name="text" required>
    <button type="submit">Отправить</button>
  </form>
  <p>{{ status }}</p>

  <form method="post" action="/load">
    <button type="submit">Получить данные</button>
  </form>
  <textarea rows="10" cols="50" readonly>{{ content }}</textarea>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(PAGE, status="", content="")


@app.post("/send")
def send():
    try:
        response = requests.post(f"{BACKEND_URL}/data", json={"text": request.form["text"]}, timeout=5)
        status = "Отправлено" if response.ok else f"Ошибка бэкенда: {response.status_code}"
    except requests.RequestException:
        status = "Бэкенд недоступен"
    return render_template_string(PAGE, status=status, content="")


@app.post("/load")
def load():
    try:
        response = requests.get(f"{BACKEND_URL}/data", timeout=5)
        content = response.json()["content"] if response.ok else f"Ошибка бэкенда: {response.status_code}"
    except requests.RequestException:
        content = "Бэкенд недоступен"
    return render_template_string(PAGE, status="", content=content)


if __name__ == "__main__":
    app.run(port=5000)

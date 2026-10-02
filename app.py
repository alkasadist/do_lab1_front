import os

import requests
from flask import Flask, render_template_string, request

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

app = Flask(__name__)

PAGE = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>Frontend v1.0</title></head>
<body>
  <form method="post" action="/send">
    <input name="text" required>
    <button type="submit">Отправить</button>
  </form>
  <p>{{ status }}</p>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(PAGE, status="")


@app.post("/send")
def send():
    try:
        response = requests.post(f"{BACKEND_URL}/data", json={"text": request.form["text"]}, timeout=5)
        status = "Отправлено" if response.ok else f"Ошибка бэкенда: {response.status_code}"
    except requests.RequestException:
        status = "Бэкенд недоступен"
    return render_template_string(PAGE, status=status)


if __name__ == "__main__":
    app.run(port=5000)

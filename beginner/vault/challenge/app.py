from flask import Flask, request, render_template
import time
from asgiref.wsgi import WsgiToAsgi
from asyncio import sleep

app = Flask(__name__)

PASSWORD = 'H8iObjIcSr'

@app.route("/", methods=["GET"])
async def index():
    guess = request.args.get("password", "")
    if not guess:
        return render_template("index.html", result=None, elapsed_ms=None)

    start = time.time()
    ok = await check_password(guess)
    elapsed = (time.time() - start) * 1000  # in ms

    result = None
    if ok:
        result = "Correct! Here is your flag: K17{aLL_iN_go0d_t1m3}"
    else:
        result = "Incorrect password. Try again."

    return render_template("index.html", result=result, elapsed_ms=f"{elapsed:.2f}")

async def check_password(guess):
    for i, c in enumerate(guess):
        if i >= len(PASSWORD) or c != PASSWORD[i]:
            return False
        await sleep(0.1)
    return guess == PASSWORD

asgi_app = WsgiToAsgi(app)

from flask import Flask
from threading import Thread

app = Flask("keepalive")

@app.route("/")
def index():
    return "Server started!"

def run(): app.run(host= "0.0.0.0", port= 0000)
def keep_alive():
    """Keep the bot running"""
    Thread(target= run).start()
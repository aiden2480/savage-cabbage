from flask import Flask

web = Flask(__name__)

@web.route('/')
def index():
    return 'OK!'

if __name__ == "__main__":
    web.run()
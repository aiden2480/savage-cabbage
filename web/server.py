from flask import *
web = Flask(__name__)

# Routes
@web.route('/')
def index():  return web.send_static_file('./index.html')

@web.route('/invite')
def invite(): return web.send_static_file('./invite.html')


if __name__ == "__main__":
    web.run()
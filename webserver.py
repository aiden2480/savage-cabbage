# Flask setup
from flask import *
web = Flask('Savage Cabbage Website')

# Routes
@web.route('/')
def index(): return render_template("index.html")

@web.route('/invite')
def invite(): return render_template("invite.html")


if __name__ == "__main__":
    web.run()
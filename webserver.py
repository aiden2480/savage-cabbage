# Flask setup
from flask import Flask, render_template
web = Flask('Savage Cabbage Website')

# Commands setup
from util import CMDS, CMD_CLASSES

# Routes
@web.route('/')
def index(): return render_template("index.html", cmds= CMDS, cmd_classes= CMD_CLASSES)

@web.route('/invite')
def invite(): return render_template("invite.html")


if __name__ == "__main__":
    web.run()
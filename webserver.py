# Flask setup
from flask import Flask, render_template
web = Flask('Savage Cabbage Website')

# Commands setup
from setup import (
    CMDS, CMD_CLASSES,
    BOT_INVITE_LINK, SUPPORT_SERVER_INVITE,
    CLASS_CMDS, run_time,
)

# Routes
@web.route('/') # Static link
def index(): return render_template("index.html",
    cmds= CMDS, cmd_classes= CMD_CLASSES,
    class_cmds= CLASS_CMDS, run_time= run_time[0],
)

@web.route('/invite') # Redirect link
def invite(): return render_template("redirect.html",
    title= "Invite Savage Cabbage",
    redirect= BOT_INVITE_LINK
)

@web.route('/server-invite') # Redirect link
def server_invite(): return render_template("redirect.html",
    title= "Savage Cabbage Support Server",
    redirect= SUPPORT_SERVER_INVITE
)


if __name__ == "__main__":
    web.run()
# Flask setup
from flask import Flask, send_file, render_template
web = Flask('Savage Cabbage Website')

# Logging setup
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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
    redirect= BOT_INVITE_LINK,
    embed_title= "Invite Savage Cabbage to your server!",
    embed_description= "yay!",
)

@web.route('/server-invite') # Redirect link
def server_invite(): return render_template("redirect.html",
    title= "Savage Cabbage Support Server",
    redirect= SUPPORT_SERVER_INVITE,
    embed_title= "Join Savage Cabbage's support server!",
    embed_description= "Join for help with any of the commands, to report a bug or to use the custom commands!",
)

@web.route('/static/icon') # For reference
def icon(): return send_file("static/icon.jpg",
    mimetype= 'image/gif'
)


# Yeet that online!
if __name__ == "__main__":
    web.run()
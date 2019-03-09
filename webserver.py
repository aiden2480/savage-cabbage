# Flask setup
import sys
import flask
import threading
import random as r
from discord.ext import commands
web = flask.Flask("Savage Cabbage Website", 
    template_folder= "web/templates",
    static_folder= "web/static",
)

# Logging setup
import logging
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


# Commands setup
from setup import (
    BOT_INVITE_LINK, SUPPORT_GUILD_INVITE,
    WEBSITE_HOMEPAGE, RUN_TIME, SOURCE_CODE,
    UPDATE_LOG, roasts_no_bold
)


# Web Routes
@web.route("/") # Static link
def index(): return flask.render_template("index.html",
    run_time= RUN_TIME,
    source_code= SOURCE_CODE,
    website_homepage= WEBSITE_HOMEPAGE,
    choice_roast= r.choice(roasts_no_bold),
)

@web.route("/log")
@web.route("/logs")
def logs(): return flask.render_template("logs.html",
    website_homepage= WEBSITE_HOMEPAGE,
    update_log= UPDATE_LOG,
    last_update= (list(UPDATE_LOG)[0], UPDATE_LOG[list(UPDATE_LOG)[0]])
)

@web.route("/invite") # Redirect link
def invite(): return flask.render_template("redirect.html",
    title= "Invite Savage Cabbage",
    redirect= BOT_INVITE_LINK,
    website_homepage= WEBSITE_HOMEPAGE,
    embed_title= "Invite Savage Cabbage to your server!",
    embed_description= "yay!",
)

@web.route("/server-invite") # Redirect link
def server_invite(): return flask.render_template("redirect.html",
    title= "Savage Cabbage Support Server",
    redirect= SUPPORT_GUILD_INVITE,
    website_homepage= WEBSITE_HOMEPAGE,
    embed_title= "Join Savage Cabbage's support server!",
    embed_description= "Join for help with any of the commands, to report a bug or to use the custom commands!",
)

@web.route("/static/icon") # For reference
def icon(): return flask.send_file("web/static/icon.jpg",
    mimetype= "image/gif"
)

@web.errorhandler(404)
def four0four(e): return flask.render_template("errors/404.html"), 404


# Yeet that online!
if __name__ == "__main__":
    web.run()
# Flask setup
import random as r
import multiprocessing
from discord.ext import commands
from flask import Flask, send_file, render_template
web = Flask("Savage Cabbage Website")

# Logging setup
import logging
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

# Bot setup
bot: commands.Bot

# Commands setup
from setup import (
    BOT_INVITE_LINK, SUPPORT_GUILD_INVITE,
    WEBSITE_HOMEPAGE, RUN_TIME, SOURCE_CODE,
    UPDATE_LOG, roasts_no_bold
)

# Web Routes
@web.route("/") # Static link
def index(): return render_template("index.html",
    run_time= RUN_TIME,
    source_code= SOURCE_CODE,
    website_homepage= WEBSITE_HOMEPAGE,
    choice_roast= r.choice(roasts_no_bold)
)

@web.route("/log")
@web.route("/logs")
def logs(): return render_template("logs.html",
    website_homepage= WEBSITE_HOMEPAGE,
    update_log= UPDATE_LOG,
    last_update= (list(UPDATE_LOG)[0], UPDATE_LOG[list(UPDATE_LOG)[0]])
)

@web.route("/invite") # Redirect link
def invite(): return render_template("redirect.html",
    title= "Invite Savage Cabbage",
    redirect= BOT_INVITE_LINK,
    website_homepage= WEBSITE_HOMEPAGE,
    embed_title= "Invite Savage Cabbage to your server!",
    embed_description= "yay!",
)

@web.route("/server-invite") # Redirect link
def server_invite(): return render_template("redirect.html",
    title= "Savage Cabbage Support Server",
    redirect= SUPPORT_GUILD_INVITE,
    website_homepage= WEBSITE_HOMEPAGE,
    embed_title= "Join Savage Cabbage's support server!",
    embed_description= "Join for help with any of the commands, to report a bug or to use the custom commands!",
)

@web.route("/static/icon") # For reference
def icon(): return send_file("static/icon.jpg",
    mimetype= "image/gif"
)


# Yeet that online!
def run():web.run(debug= True)
def start_server(BOT):
    """Start the webserver for the website (this also helps keep the bot online)"""
    global bot
    bot = BOT

    multiprocessing.Process(target= run, daemon= True).start()


if __name__ == "__main__": web.run(debug= True)
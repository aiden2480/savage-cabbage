# Flask setup
import flask
import threading
import random as r
from discord.ext import commands
web = flask.Flask("Savage Cabbage Website")

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

command_info = {
    "general": [["help", "stop it, get some help"], ["info", "stats about the bot"], ["suggest", "send a helpful suggestion!"]],
    
    "memey": [["meme", "get the freshest memes off reddit"], ["vr", "image manipulation of the classic vr template"], ["spongebob", "just you wait and see"]],
    
    "currency": [["daily", "1k coins, once a day"], ["steal", "steal from another user, spoopy"], ["bank", "view the contents of your bank"]],
}


# Web Routes
@web.route("/") # Static link
def index():
    # print(bot.cogs)
    command_info= {}
    for cog in bot.cogs:
        command_info[cog]= []
        for cmd in cog.get_commands():
            if not cmd.hidden and cmd.enabled:
                command_info[cog].append([cmd.name, cmd.help])
    
    return flask.render_template("index.html",
        bot= bot,
        run_time= RUN_TIME,
        source_code= SOURCE_CODE,
        command_info= command_info,
        website_homepage= WEBSITE_HOMEPAGE,
        choice_roast= r.choice(roasts_no_bold),
        bot_stats= (len(list(bot.get_all_members())), len(bot.guilds)),
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
def icon(): return flask.send_file("static/icon.jpg",
    mimetype= "image/gif"
)


# Yeet that online!
def run():
    web.run(host= "0.0.0.0", port= 0000)
def start_server(BOT):
    """Start the webserver to keep this bot online! (but since I"""
    global bot
    bot = BOT

    threading.Thread(target= run).start()


if __name__ == "__main__":
    bot = commands.Bot("test bot")
    web.run(debug= True)

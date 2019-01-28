# Imported at the beginning, referenced to but not changed

import os
import praw

try:
    import dotenv
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env")) # Load .env file for local testing
except ModuleNotFoundError: pass # 'dotenv' not in requirements.txt so this snippet won't run

reddit = praw.Reddit(
    user_agent= "Reddit Searching for Savage Cabbage#3666",
    client_id= os.getenv("REDDIT_ID"),
    client_secret= os.getenv("REDDIT_TOKEN"),
)

class emojis:
    partyparrot = '<a:partyparrot:538925147634008067>'

# Attribute Dictionary function (for accessing values as attributes)
class AttrDict(dict):
    def __getattr__(self, attr): return self[attr]
    def __setattr__(self, attr, value): self[attr] = value

roasts = [
    # "Oof!",
    "Hecc off!",
    "You are a dirt puddle!",
    "Go commit **neck-rope**",
    "Go commit **bullet-face**",
    "You're fatter than big smoke",
    "Go commit **choke-on-water**",
    "You are smelly and not very smart",
    "You have a face made for **radio**",
    "Go commit **oxygen-not-reach-lung**",
    "Go commit **food-not-reach-stomach**",
    "You're so ugly that Hello Kitty said **goodbye** to you",
    # "I've seen some pricks in my life, but **you're a cactus!**",
    "You're as useless as **ejection seats** on a **helicopter**",
    "You bring everyone a lot of joy, when you **leave the room**",
    "If what you don't know can't hurt you, you must be **invulnerable!**",
    "Somebody once told me that you aren't the sharpest tool in the shed",
    "You've got a photographic memory but **with the lens cover glued on**",
    "Roses are red, Violets are blue, God made me pretty, **What happened to you**?",
    "There are several people in this world that I find obnoxious and you are **all of them**",
    "Somewhere out there is a tree, tirelessly producing oxygen so you can breathe. **I think you owe it an apology**"
    # "You're as straight as the pole your mum dances on"
]

eightball_answers = [
    # Yes
    "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Duh, of course"
    # Maybe
    "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "whaaaaat? y u no *concentrate*?", 
    # No
    "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful.", "Heck no", "u wish", 
]


commands_run= commands_run_not_admin= 0
roasts_str= ""

one_in_what= 15
greetings= ["Hey", "Yo", "Wassup", "Oi"]
roasts_no_bold= [roast.replace("**", "") for roast in roasts]
for roast in roasts_no_bold:
    roasts_str+= f"{roast}\n"
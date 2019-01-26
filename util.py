# Message setup function #
async def message_setup(m, client):
    _devs = [
        await client.get_user_info(id)
        for id in [
            272967064531238912,  # Get
            270138433370849280,  # users
            297229962971447297,  # ID,
            499740673424097303,  # but who?
        ]
    ]

    _admin = m.author in _devs
    _msg = m.content
    _cmd = _msg.split()[0][1:].lower()
    _args = _msg.split()[1:]

    return _devs, _admin, _msg, _cmd, _args


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
    "If what you don't know can't hurt you, you must be **invunreble!**",
    "Somebody once told me that you aren't the sharpest tool in the shed",
    "You've got a photographic memory but **with the lens cover glued on**",
    "Roses are red, Violets are blue, God made me pretty, **What happened to you**?",
    "There are several people in this world that I find obnoxious and you are **all of them**",
    "Somewhere out there is a tree, tirelessly producing oxygen so you can breathe. **I think you owe it an apology**"
    # "You're as straight as the pole your mum dances on"
]

one_in_what = 15
greetings = ["Hey", "Yo", "Wassup", "Oi"]
roasts_no_bold = [i.replace("**", "") for i in roasts]
roasts_str = ""
for i in roasts_no_bold:
    roasts_str += i + "\n"

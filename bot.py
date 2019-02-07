# Importing #
import os
import sys
import time
import random
import discord
import asyncio
import requests


# Setup Vars #
from setup import *
client = discord.Client(shard_count= SHARD_COUNT)

# Setup Events #
@client.event # Error handling
async def on_error(event, args):
    if type(args) == discord.Message:
        m, tb= args, sys.exc_info() # The error is usually a message so args is usually a discord Message
        devs, admin, total_users, in_support_server= await message_setup(m, client)
        embed= discord.Embed(title= f"An error occoured during the **{event}** event", color= 0xFF8C00)

        fields= {
            "Message": [f"```{m.content}```", False],
            "Error": [f"```py\n{tuple(tb)[0].__name__}: {tb[1]}```", False],
            "Traceback": [f"```py\n{tb_to_str(tb)}```", True], # Traceback object, need to get str
            "Author": [m.author, True],
            "Server": [m.server, True],
            "Channel": [m.channel, True]}
        
        embed.set_thumbnail(url= m.server.icon_url)
        embed.set_author(name= m.author, icon_url= m.author.avatar_url)
        for field in fields: embed.add_field(name= field, value= fields[field][0], inline= fields[field][1])
        await client.send_message(discord.Object(542474215282966549), embed= embed)
        await client.send_message(m.channel, embed= discord.Embed(
            title= "💣 Oof, an error occoured 💥",
            description= f"Please [join the support server](https://savage-cabbage.herokuapp.com/server-invite) and tell **{devs[0]}** what happened to help fix this bug",
            color= 0xFFA500,
        ))

@client.event # Log joining a server
async def on_server_join(server: discord.Server):
    print(f"Joined a server: {server.name}, members: {server.member_count}")
    embed= discord.Embed(
        title= "Server join",
        description= f"Joined **{server.name}** (**{server.member_count- 1}** other members)",
        color= 0x228B22)

    embed.set_thumbnail(url= server.icon_url)
    embed.add_field(name= "Server Members", value= server.member_count, inline= True)
    embed.add_field(name= "New Total Servers", value= len(client.servers), inline= True)
    await client.send_message(discord.Object(542474215282966549), embed= embed)

@client.event # Log leaving a server
async def on_server_remove(server: discord.Server):
    print(f"Kicked from a server: {server.name}, members: {server.member_count}")
    embed= discord.Embed(
        title= "Kicked from server",
        description= f"Kicked from **{server.name}** (**{server.member_count- 1}** other members)",
        color= 0xf44e42)

    embed.set_thumbnail(url= server.icon_url)
    embed.add_field(name= "Server Members", value= server.member_count, inline= True)
    embed.add_field(name= "New Total Servers", value= len(client.servers), inline= True)
    await client.send_message(discord.Object(542474215282966549), embed= embed)

# Main Events #
@client.event # Setup function
async def on_ready():
    global current_status
    _ = 0
    for server in client.servers:
        for user in server.members:
            _ += 1

    print(f"\tLogged in as {client.user}\n\tTime run: {run_time[0]}") # \n\tServer count: {len(client.servers)}\n\tUser count: {_}")

    current_status = await change_status(client, await client.get_user_info(272967064531238912)) # f"$help |~| Insulting {total_users} users across {len(client.servers)} servers |~| {random.choice(roasts_no_bold)}"

@client.event # Main event (houses commands)
async def on_message(m: discord.Message):
    if m.author.bot: return
    msg, send= m.content, SendEmbed(m, client).Send
    global commands_run, commands_run_not_admin, current_status


  # Commands (must go last because of how it's set up)
    # Command setup vars, return if not command
    if msg.lower().startswith('$') or msg.lower().startswith(client.user.mention):
        try:
            if msg.lower().startswith('$'):
                cmd, args= msg[1:].split()[0].lower(), msg[1:].split()[1:]
            else:
                cmd, args= msg[21:].split()[0].lower(), msg[21:].split()[1:]
        except: return # Not command and prefix is a coincidence
        devs, admin, total_users, in_support_server= await message_setup(m, client)
        
        if cmd in CMDS:
            print('Command run:', m.author, cmd, " ".join(args))

            await send("Command run",
                f"```{msg}```",
                channel= discord.Object(542961329867063326),
                color= 0xf9e236,
                sendTyping= False,
                set_author_img= True,
                fields= {"User": m.author, "Server": m.server, "Channel": m.channel}
            )

            commands_run += 1
            if not admin: commands_run_not_admin += 1

    # General commands
        if cmd in ["help"] + CMDS.help[1]:
            if not args:
                return await send(":tools: Help :gear:",
                    f"""
                    Every time a message is sent, there is a one in **{one_in_what}** chance that the messenger will be insulted (Send `$roast list` for the insults)
                    To prevent a user from being roasted, add `don't roast the roaster` to thier roles

                    Please consider upvoting [here](https://discordbotlist.com/bots/492873992982757406/upvote) (Once per 24 hrs)
                    """)

            args = [arg.lower() for arg in args]
            try:
                _ = ''
                for alias in CMDS[args[0]][1]:
                    _ += str(alias)+ ', '

                await send(f":tools: Help for command **{args[0]}** :gear:",
                    CMDS[args[0]][0],
                    footer= "Aliases: "+ _[:-2])

            except KeyError:
                await send("", "lol that command doesn't exist")

        elif cmd in ["info"] + CMDS.info[1]:
            _ = [time.time() - run_time[1], 'seconds']
            if _[0] >= 86400: _ = [_[0]/86400, 'days']
            elif _[0] >= 3600: _ = [_[0]/3600, 'hours']
            elif _[0] >= 60: _ = [_[0]/60, 'minutes']
            _ = [round(_[0], 3), _[1]]

            await send(":information_source: Info :thinking:",
                f"Here's the info for **{client.user}**",
                footer= f"Last restart {_[0]} {_[1]} ago",
                fields= {
                    "Developer :computer:": devs[0],
                    # "Admins :tickets:": "%s &\n%s" % (devs[1], devs[2]), # Thier names are too long for my poor info message
                    "Servers :homes:": len(client.servers),
                    "Total users :busts_in_silhouette:": total_users,
                    "Version :white_check_mark:": BOT_VERSION,
                    "Last restart :calendar:": run_time[0],
                    "Region :earth_asia:": "Australia",
                    "Code platform :bow_and_arrow:": "GitHub",
                    "Hosting service :dart:": "Heroku",
                    "Language :airplane:": "discord.py async\nPython 3.7",
                })

            if admin:
                await send('Admin Info', "",
                    fields= {
                        "Commands run": commands_run,
                        "Commands not run by a dev": commands_run_not_admin},
                    sendTyping= False)

        elif cmd in ["status"] + CMDS.status[1]:
            await client.send_typing(m.channel)
            await asyncio.sleep(0.75)
            if admin and args:  _ = await change_status(client, devs[0], ' '.join(args))
            else: _ = await change_status(client, devs[0])

            await send('Status changed to **{} {}**'.format({0:'Playing',1:'Streaming',2:'Listening to',3:'Watching'}[_[0]],_[1]),
                "",
                footer= "Want to suggest a status? Use $suggest in a DM!",
                sendTyping= False)

        elif cmd in ["invite"] + CMDS.invite[1]:
            await send("**:mailbox_with_mail: Invite :homes:**",
                f"""Invite me to your server [here]({BOT_INVITE_LINK})
                Join my support server: {SUPPORT_SERVER_INVITE}""")

        elif cmd in ["vote"] + CMDS.vote[1]:
            await send("**:arrow_up: Upvote links :newspaper2:**",
                " - [**Discord Bot List**](https://discordbotlist.com/bots/492873992982757406/upvote)")

        elif cmd in ["commands", "cmds"]:
            #await send("", "Use `$help` for help or see all my commands on my website:")
            await client.send_message(m.channel, "Use `$help` for help or see all my commands on my website: https://savage-cabbage.herokuapp.com/#cmds")

    # DM commands
        elif cmd in ["suggest"] + CMDS.suggest[1]:
            if m.server == None:
                if args:
                    await send(f"Suggestion from {m.author}",
                        f"{m.author.mention}: **{' '.join(args)}**",
                        channel= discord.Object(502963219879559168))

                    await send( "Suggestion recevied", "kewlio")
                else: await send('', "Were you going to suggest anything? 🤷‍")
            else: await send('', 'lol this is a DM command noob')

    # Roast commands
        elif cmd in ["roast"] + CMDS.roast[1]:
            if not args:
                await send(random.choice(greetings) + " " + m.author.name + ",",
                    random.choice(roasts))

            elif args[0].lower() == 'list':
                await send("You asked for it buddy",
                    roasts_str.replace('\n', '\n\n'))

            else:
                await send(random.choice(greetings) + " " + " ".join(args) + ",",
                    random.choice(roasts))

    # Meme commands
        elif cmd in ["meme"] + CMDS.meme[1]:
            _ = time.time()
            await client.send_typing(m.channel)

            while True:
                r_sub = reddit.subreddit("+".join([
                    #"meirl", "me_irl",
                    "dankmemes"#, "PrequelMemes",
                    #"Hmmm", "wholesomememes",
                    #"MinecraftMemes", "ROBLOXmemes",
                    #"DeepFriedMemes",
                ])).random()

                if r_sub.url.endswith(".png") or r_sub.url.endswith(".jpg"):
                    reddit_embed = discord.Embed(title= r_sub.title)
                    reddit_embed.set_image(url= r_sub.url)
                    reddit_embed.set_footer(text= f"⬆ {r_sub.score} 💭 {r_sub.num_comments}")

                    await client.send_message(m.channel, embed= reddit_embed)
                    break
                else: continue
    
    # Image commands
        elif cmd in ['imgur'] + CMDS.imgur[1]:
            if not args: args = [random.choice(["memes", "birbs", "doggos"])] # Need to add more topics
            imgur_data= requests.get(f"https://api.imgur.com/3/gallery/r/{args[0]}",
                headers= {"Authorization": imgur_auth}).json()["data"]

            try:
                imgur_submission= imgur_data[random.randint(1, 99)] # Control selection avaliable
                await send(imgur_submission["title"],
                    "",
                    image= imgur_submission["link"],
                    footer= f"👀{imgur_submission['views']} 👍{imgur_submission['score']}")
            except: await send("", "oof, no results :shrug:")

    # Fun commands
        elif cmd in ['8ball'] + CMDS['8ball'][1]:
            if args:
                await send(f':8ball: {m.content} :rabbit2:',
                    random.choice(eightball_answers))
            else:
                await send('', 'What did you want to ask the all-mighty 8ball? (c to cancel)')
                _ = await client.wait_for_message(author= m.author)
                if _.content != 'c':
                    await send(f':8ball: {" ".join(args)} :rabbit2:',
                        random.choice(eightball_answers))

        elif cmd in ["spr"] + CMDS.spr[1]:
            if not args: return await send('', 'lol u need to play from scissors, paper and rock')
            if not args[0].lower() in ['scissors', 'paper', 'rock', '✂', '📰', '🗞']:
                return await send('', 'lol u need to play from scissors, paper and rock')
            args[0] = args[0].lower()

            _ = random.choice(['scissors', 'paper', 'rock'])
            args[0] = {'✂': 'scissors', '📰': 'paper', '🗞': 'paper'}[args[0]]

            if args[0] == _: result = "It's a tie!"
            elif args[0] == 'scissors' and _ == 'paper': result = 'You win!'
            elif args[0] == 'paper' and _ == 'rock': result = 'You win!'
            elif args[0] == 'rock' and _ == 'scissors': result = 'You win!'
            else: result = 'I win!'

            await send(f':scissors: SPR with {m.author} :newspaper:',
                f"I chose **{_}** and you chose **{args[0]}**, **{result}**")

    # Text commands
        elif cmd in ["partyparrot"] + CMDS.partyparrot[1]:
            if args: await send('', str(emojis.partyparrot).join(args))
            else: await send('', f'What do you want me to {emojis.partyparrot}?')


client.run(os.getenv("BOT_TOKEN"))
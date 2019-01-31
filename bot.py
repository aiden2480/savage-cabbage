# Importing #
import os
import time
import random
import discord
import asyncio
from setup import *

# Setup #
client = discord.Client()

# Events #
@client.event
async def on_ready():
    global current_status
    _ = 0
    for server in client.servers:
        for user in server.members:
            _ += 1

    print(f"\tLogged in as {client.user}\n\tTime run: {run_time[0]}\n\tServer count: {len(client.servers)}\n\tUser count: {_}")
    
    current_status = await change_status(client, await client.get_user_info(272967064531238912)) # f"$help |~| Insulting {total_users} users across {len(client.servers)} servers |~| {random.choice(roasts_no_bold)}"

@client.event
async def on_message(m):
    msg= m.content
    if m.author.bot: return
    global commands_run, commands_run_not_admin, current_status

  # Send function
    async def send(title, message, footer= None, fields= {}, channel= m.channel, sendTyping= True):
        if sendTyping:
            await client.send_typing(channel)
            await asyncio.sleep(0.75)

        embed = discord.Embed(
            title= title,
            description= message,
            color= discord.Color(random.randint(0, 0xFFFFFF)),
        )

        if footer: embed.set_footer(text= footer)
        for field in fields.keys(): embed.add_field(name= field, value= fields[field])
        
        await client.send_message(channel, embed= embed)

  # Commands (must go last because of how it's set up)
    # Command setup vars, return if not command
    if msg.lower().startswith('$') or msg.lower().startswith(client.user.mention):
        try:
            if msg.lower().startswith('$'):
                cmd= msg[1:].split()[0].lower()
                args= msg[1:].split()[1:]
            else:
                cmd= msg[21:].split()[0].lower()
                args= msg[21:].split()[1:]
        except: return # Not command and prefix is a coincidence
        devs, admin, total_users, in_support_server = await message_setup(m, client)
        if cmd in CMDS: print('Command run:', m.author, cmd, " ".join(args))
        commands_run += 1
        if not admin: commands_run_not_admin += 1
    # Now the actual commands

    # General commands
        if cmd in ["help"] + CMDS.help[1]:
            if not args:
                return await send(":tools: Help :gear:",
                    f"""
                    Every time a message is sent, there is a one in **{one_in_what}** chance that the messenger will be insulted (Send `$roast list` for the insults)
                    To prevent a user from being roasted, add `don\'t roast the roaster` to thier roles
                
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
            
            await send("🇮 Info :thinking:",
                f"""Created by {devs[0].mention} (**{devs[0]}**)
                Admins: {devs[1].mention} (**{devs[1]}**) & {devs[2].mention} (**{devs[2]}**)
                
                Total servers: **{len(client.servers)}**\nTotal users: **{total_users}**""",
                footer= f"Last refresh: {run_time[0]} AEST ({_[0]} {_[1]} ago)")
            
            await send("🇮 Info :thinking:",
                f"Here's the info for **{client.user}**",
                footer= f"Last refresh {_[0]} {_[1]} ago",
                fields= {
                    "Developer :computer:": devs[0],
                    #"Admins :tickets:": "%s &\n%s" % (devs[1], devs[2]), # Thier names are too long for my poor info message
                    "Servers :homes:": len(client.servers),
                    "Total users :busts_in_silhouette:": total_users,
                    "Version :white_check_mark:": BOT_VERSION,
                    "Last restart :calendar:": run_time[0],
                    "Region :earth_asia:": "Australia",
                    "Code platform :bow_and_arrow:": "GitHub",
                    "Hosting service :dart:": "Heroku",
                    "Language :airplane:": "discord.py async\nPython 3.7"
                })
            
            if admin:
                await send('Admin Info', '',
                    fields= {"Commands run": commands_run,
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
                f"""Invite me to your server [here](https://discordapp.com/oauth2/authorize?client_id=492873992982757406&scope=bot&permissions=201641024)
                Join my support server: https://discord.gg/AJj45Sj""")

        elif cmd in ["vote"] + CMDS.vote[1]:
            await send("**:arrow_up: Upvote :newspaper2:**",
                " - [**Discord Bot List**](https://discordbotlist.com/bots/492873992982757406/upvote)")

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
        elif cmd in ["reddit"] + CMDS.reddit[1]:
            _ = time.time()
            await client.send_typing(m.channel)

            while True:
                r_sub = reddit.subreddit("+".join([
                    "meirl", "me_irl",
                    "dankmemes", "PrequelMemes",
                    "Hmmm", "wholesomememes",
                    "MinecraftMemes", "ROBLOXmemes",
                    "DeepFriedMemes",
                ])).random()

                if r_sub.url.endswith(".png") or r_sub.url.endswith(".jpg"):
                    reddit_embed = discord.Embed(title= r_sub.title)
                    reddit_embed.set_image(url= r_sub.url)
                    reddit_embed.set_footer(text= f"⬆ {r_sub.score} 💭 {r_sub.num_comments}")

                    await client.send_message(m.channel, embed= reddit_embed)
                    if m.author in devs:
                        await send('',str(round(time.time()-_, 3))+ ' sec',
                            sendTyping= False)
                    break
                else: continue

    # Fun commands
        elif cmd in ['8ball'] + CMDS['8ball'][1]:
            if args:
                await send(f':8ball: {m.content} :rabbit2:',
                    random.choice(eightball_answers))
            else:
                await send('', 'What did you want to ask the all-mighty 8ball? (c to cancel)')
                _ = await wait_for_message(author= m.author)
                if _.content != 'c':
                    await send(f':8ball: {m.content} :rabbit2:',
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
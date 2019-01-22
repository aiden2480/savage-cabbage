#    _________                                           #
#   /   _____/____ ___  _______     ____   ____          #
#   \_____  \\__  \\  \/ /\__  \   / ___\_/ __ \         #
#   /        \/ __ \\   /  / __ \_/ /_/  >  ___/         #
#  /_______  (____  /\_/  (____  /\___  / \___  >        #
#          \/     \/           \//_____/      \/         #
#  ________       ___.  ___.                             #
#  \_   ___ \_____ \_ |__\_ |__ _____     ____   ____    #
#  /    \  \/\__  \ | __ \| __ \\__  \   / ___\_/ __ \   #
#  \     \____/ __ \| \_\ \ \_\ \/ __ \_/ /_/  >  ___/   #
#   \______  (____  /___  /___  (____  /\___  / \___  >  #
#          \/     \/    \/    \/     \//_____/      \/   #

# - Please report bugs to Savage Cabbage on discord via a DM with
# 	the content `$bug <description>`
# - To suggest a roast, message @Savage Cabbage#2793 on discord
# 	in a DM - with the message `$suggest <idea>`
# - https://www.rappad.co/insult-generator for roast ideas
# - Blame Flynn ¯\_(ツ)_/¯ (͡° ͜ʖ ͡°)


# Importing modules, variables and setup #
import os, random, discord, asyncio
from data._util import roasts, message_colours, time
from data._util import * # one_in_what, greetings, no_auto_roast_servers, roasts_str, roasts_no_bold, start_server
client = discord.Client()
repl_started = time.repl_started()

# Once setup finished, event #
@client.event
async def on_ready():
  server_started = time.server_started()

  global total_users
  total_users = 0
  for server in client.servers:
    for user in server.members: total_users += 1

  print(f"""\n
  |===============================|
  | Discord.py up, Server started |
  | I'm in as {client.user} |
  |===============================|
  | Server start time: {round(server_started-repl_started,3)} sec |
  | HTTP Requests,data and errors |
  |===============================|
  
  \tServer count: {len(client.servers)}
  \tMember count: {total_users}
  \n""")

  await client.change_presence(game=discord.Game(name=
    f"$help |~| Insulting {total_users} users across {len(client.servers)} servers |~| {random.choice(roasts_no_bold)}"
  ))

# Other Events #
@client.event
async def on_message(m):
  blacklisted = []

  # Blacklisting
  if m.author.bot or m.author in blacklisted: return

  # Variables
  rand = random.randint(1, one_in_what)
  msg = m.content
  devs = [await client.get_user_info(id) for id in [272967064531238912,270138433370849280,297229962971447297,499740673424097303]]
  try: roles = [y.name.lower() for y in m.author.roles]
  except AttributeError: roles = []

	# Functions
  async def send(title,message,footer=None,channel = m.channel):
    message_embed = discord.Embed(
      title = title,
      description = message,
      color = random.choice(message_colours),
    )

    if footer: message_embed.set_footer(text=footer)
    await client.send_message(channel, embed=message_embed)

  for i in msg.lower().split():
    if i in ['nou','no u']:
      try:
        nou_name = m.author.name
        await client.change_nickname(m.author,'gay')
        #await send('','Oh noes, you said the cancer word!')
        await asyncio.sleep(60)
        await client.change_nickname(m.author,nou_name)
      except: return

  if m.server == None and msg.startswith('$alert '):
    if len(msg.split()) >= 2:
      await send('Suggestion recieved from '+m.author.name, '{} has suggested **{}**'.format(m.author.mention,msg[9:]), channel = discord.Object(502963219879559168))
      await send('',f"Your message **{msg[9:]}** has been recorded, you'll recieve a reply shortly")
      return
    else:
      await send('','Were you going to alert anything or not?')
      return

  if msg.startswith('$') or msg.startswith(client.user.mention): # Command
    if msg.startswith('$'):
      cmd = msg.split()[0][1:]
      args = msg.split()[1:]
    else:
      cmd = msg.split()[0][21:]
      args = msg.split()[21:]

    if cmd == 'thotbgone' and m.author in devs:
      await send('','Fine, I\'m leaving')
      await client.leave_server(m.server)

    if cmd == 'help':
      await client.send_typing(m.channel)
      await asyncio.sleep(1.25)
      #await send('Help',f'Every time a message is sent, there is a one in **{one_in_what}** chance that the messenger will be insulted.\nTo prevent a user from being roasted, simply add `Don\'t roast the roaster` to thier roles. If you want to bypass the one in **{one_in_what}** statement and get oofed, just mention the bot in a message or type `$roast`. To roast someone else, type `$roast @user`.\n\n To suggest a new roast, message me with the contents `$alert <message>`.\n\nPlease consider upvoting [here](https://discordbotlist.com/bots/492873992982757406/upvote) (Once per 24 hrs)')
      await send(':tools: Help :wrench:',f'**\n🇮 Info :thinking:**\nEvery time a message is sent, there is a one in **{one_in_what}** chance that the messenger will be insulted (Send `$roasts` for the insults)\nTo prevent a user from being roasted, add `don\'t roast the roaster` to thier roles\n\nPlease consider upvoting [here](https://discordbotlist.com/bots/492873992982757406/upvote) (Once per 24 hrs)\nCreated by {devs[0].mention} ({devs[0]})\nAdmins: {devs[1].mention} ({devs[1]}) & {devs[2].mention} ({devs[2]})\nTotal servers: **{len(client.servers)}**\nTotal users: **{total_users}**')

    if cmd == 'info':
      await send('Info','Created by {}\nAdmins: {} & {}\nTotal servers: **{}**\nTotal users: **{}**'.format(devs[0].mention,devs[1].mention,devs[2].mention,len([i for i in client.servers]),total_users))

    if cmd in ['insults','roasts']:
      await send('Here ya go',roasts_str)

    if cmd in ['recent','news','updates']:
      await send('Recent updates','**v0.3** - Post-update bugs fixed!\n**v0.4 - Hecc, more bugs**')

    if cmd in ['status']:
      if m.author not in devs: return await send('','Lol u can\'t do that (admins only) :wink:')
      await client.send_typing(m.channel)
      await asyncio.sleep(0.75)
      await client.change_presence(game=discord.Game(name="$help |~| Insulting {} users across {} servers |~| {}".format(total_users, len(client.servers), ' '.join(args))))
      await send('','I changed my status to **{}**'.format(' '.join(args)))

    if cmd in ['roast']:
      if args == []:
        await send(random.choice(greetings) + ' ' + str(m.author.name) + ',',random.choice(roasts))
      if args[0] != '':
        await send(random.choice(greetings) + ' ' + str(await client.get_user_info(msg[2])) + ',',random.choice(roasts))

  elif '<@492873992982757406>' in msg: # Bot mentioned
    await client.send_typing(m.channel)
    await asyncio.sleep(0.5)
    await send(random.choice(greetings) + ' ' + str(m.author)[:-5] + ',',random.choice(roasts))

  elif "don't roast the roaster" in roles or "dont roast the roaster" in roles or m.author == client.user or m.author.bot: return # Other conditions

  elif rand == 1 and m.server.name not in no_auto_roast_servers: # (And as long as none of the above conditions are met)
    await client.send_typing(m.channel)
    await asyncio.sleep(0.5)
    await send(random.choice(greetings) + ' ' + str(m.author.name) + ',',random.choice(roasts))


start_server()
client.run(os.getenv("BOT_TOKEN"))
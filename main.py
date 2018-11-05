# Importing #
import os, random, discord, asyncio
from data._functions import roasts, message_colours

# Local setup #
client = discord.Client()

# Server setup #
from data import _util as util

# Variables and data #
one_in_what = 15
greetings = ['Hey','Yo','Wassup','Oi']
no_auto_roast_servers = ['Experimental']

roasts_no_bold = [i.replace('**','') for i in roasts] 
roasts_str = ''
for i in roasts_no_bold:
  roasts_str += i + '\n'

# Once setup finished, event #
@client.event
async def on_ready():

  global total_users
  total_users = 0
  for server in client.servers:
    for user in server.members:
      total_users += 1

  print("\n\n{0}\n| Discord.py up, Server started |\n| I'm in as {1} |\n{0}\n| HTTP Requests,data and errors |\n{0}\n\n".format('|'+('='*31)+'|',client.user))

  await client.change_presence(game=discord.Game(name=
    "$help |~| Insulting {} users across {} servers |~| {}"
    .format(total_users,len(client.servers),random.choice(roasts_no_bold))))

# Events #


@client.event
async def on_message(m):

  # No Bots allowed!
  if m.author.bot: return
  try: print('{}~{}~{}: {}'.format(m.server, m.channel, m.author, m.content))
  except: pass

  # Variables
  rand = random.randint(1, one_in_what)
  msg = m.content
  devs = [await client.get_user_info(id) for id in [272967064531238912,270138433370849280,297229962971447297,499740673424097303]]
  try: roles = [y.name.lower() for y in m.author.roles]
  except AttributeError: roles = []

	# Functions
  def send(title,message,channel = m.channel):
    return client.send_message(channel, embed=discord.Embed(
      title = title,
      description = message,
      color = random.choice(message_colours),
    ))

  if m.server == None:
    if msg.startswith('$suggest'):
      if len(msg.split()) >= 2:
        await send('Suggestion recieved from '+m.author.name, '{} has suggested **{}**'.format(m.author.mention,msg[9:]), channel = discord.Object(id = 502963219879559168))
        await send('Suggestion recieved',"Your suggestion **{}** has been recorded, you'll recieve a reply shortly".format(msg[9:]))
        return
      else:
        await send('','Were you going to suggest anything or not?')
        return
    
    if msg.startswith('$bug'):
      if len(msg.split()) >= 2:
        await send('Bug found by '+m.author.name, '{}: **{}**'.format(m.author.mention,msg[5:]), channel = discord.Object(id = 502963219879559168))
        await send('Bug recieved',"Your bug **{}** has been pointed out to the devs, you'll recieve a reply shortly".format(msg[5:]))
        return
      else:
        await send('','Did you have a bug to report?')
        return

  if msg.startswith('$') or msg.startswith('<@492873992982757406>'): # Command
    if msg.startswith('$'):
      cmd = msg.split()[0][1:]
      args = msg.split()[1:]
    else:
      cmd = msg.split()[0][21:]
      args = msg.split()[21:]

    if cmd == 'help':
      await client.send_typing(m.channel)
      await asyncio.sleep(1.25)
      await send('Help','Every time a message is sent, there is a one in **' + str(one_in_what) + '** chance that the messenger will be insulted.\nTo prevent a user from being roasted, simply add `Don\'t roast the roaster` to thier roles. If you want to bypass the one in **' + str(one_in_what) + '** statement and get oofed, just mention the bot in a message or type `$roast`. To roast someone else, type `$roast @user`.\n\n To suggest a new roast, message me with the contents `$suggest <suggestion>`.\n\nPlease consider upvoting [here](https://discordbotlist.com/bots/492873992982757406/upvote) (Once per 24 hrs)')
      await send(':tools: Help :wrench:','**\n🇮 Info :thinking:**\nEvery time a message is sent, there is a one in **{}** chance that the messenger will be insulted (Send `$roasts` for the insults`\n\n\nCreated by {}\nAdmins: {} & {}\nTotal servers: **{}**\nTotal users: **{}**'.format(one_in_what,devs[0].mention,devs[1].mention,devs[2].mention,len([i for i in client.servers]),total_users))

    if cmd == 'info':
      await send('Info','Created by {}\nAdmins: {} & {}\nTotal servers: **{}**\nTotal users: **{}**'.format(devs[0].mention,devs[1].mention,devs[2].mention,len([i for i in client.servers]),total_users))

    if cmd in ['insults','roasts']:
      await send('Here ya go',roasts_str)

    if cmd in ['recent','news','updates']:
      await send('Recent updates','**v0.3** - Post-update bugs fixed!\n**v0.4 - Hecc, more bugs**')

    if cmd == 'status':
      if m.author not in devs: return
      await client.send_typing(m.channel)
      await asyncio.sleep(0.75)
      await client.change_presence(game=discord.Game(name="$help |~| Insulting {} users across {} servers |~| {}".format(total_users, len(client.servers), ' '.join(args))))
      await send('','I changed my status to **{}**'.format(' '.join(args)))

    if cmd == 'roast':
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


util.start_server()
client.run(os.getenv("BOT_TOKEN"))

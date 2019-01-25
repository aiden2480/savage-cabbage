# Setup variables for messages #
async def message_setup(m, client, random):
    _devs = [await client.get_user_info(id) for id in [
        272967064531238912, # Get
        270138433370849280, # users
        297229962971447297, # ID,
        499740673424097303, # but who?
    ]]
    
    _admin = m.author in _devs
    _rand = random.randint(1, 15)
    _msg = m.content
    # _msg.split()[0] is the command prefix
    _cmd = _msg.split()[1].lower()
    _args = _msg.split()[2:]

    return _devs, _admin, _rand, _msg, _cmd, _args

# Send function #
async def send(title, message, footer = None, channel = m.channel):
    embed = discord.embed(
        title = title,
        description = message,
        color = random.choice(message_colours))
    
    if footer: embed.set_footer(text=footer)
    await client.send_message(channel, embed=embed)

class General:
    async def help(m):
        return await send(":tools: Help :wrench:",f"""**
        🇮 Info :thinking:**
        Every time a message is sent, there is a one in **{one_in_what}** chance that the messenger will be insulted (Send `$roasts` for the insults)
        To prevent a user from being roasted, add `don\'t roast the roaster` to thier roles
        
        Please consider upvoting [here](https://discordbotlist.com/bots/492873992982757406/upvote) (Once per 24 hrs)
        Created by {devs[0].mention} ({devs[0]})
        Admins: {devs[1].mention} ({devs[1]}) & {devs[2].mention} ({devs[2]})
        Total servers: **{len(client.servers)}**\nTotal users: **{total_users}**""")
    
    async def info(m):
        return await send('Info',f"""Created by {devs[0].mention} ({devs[0]})
        Admins: {devs[1].mention} ({devs[1]}) & {devs[2].mention} ({devs[2]})
        Total servers: **{len(client.servers)}**\nTotal users: **{total_users}**""")

class Memes():
    async def reddit(m, reddit, search = None):
        while True:
            if search: r_sub = reddit.subreddit('+'.join(args)).random()
            else: r_sub = reddit.subreddit('Unexpected').random()
            if r_sub.url.endswith('.png') or r_sub.url.endswith('.jpg'):
                reddit_embed = discord.Embed(title= r_sub.title)
                reddit_embed.set_image(url= r_sub.url)
                reddit_embed.set_footer(text= f'⭐ {r_sub.score} 💭 {r_sub.num_comments}')
                await client.send_message(m.channel, embed= reddit_embed)
                break
            else: continue

class Roasts:
    async def roast(self):
        pass
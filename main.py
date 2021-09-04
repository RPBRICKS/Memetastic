import discord, datetime, time
from discord.ext import commands
import random
from discord import Spotify
import os
import dateutil.parser
from asyncio import sleep as s 
from discord import Embed, TextChannel
import daytime
import discord 
from webserver import keep_alive
from discord.ext import commands 
import asyncio
from discord.utils import get
import requests
from discord.ext import commands, tasks
from random import choice
import json
import praw
import aiohttp
import giphy_client
from giphy_client.rest import ApiException

from PIL import Image,ImageFont,ImageDraw
from io import BytesIO


def get_prefix(client,message):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


intents = discord.Intents().all()
intents.members = True
client = commands.Bot(command_prefix = get_prefix, intents=intents)
client.remove_command('help')
start_time = time.time()
client.warnings = {} 


@client.event
async def on_guild_join(guild):


    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "!"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f)




@client.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f)    

    await ctx.send(f"The prefix was changed to {prefix}")

dj = ['What does a baby computer call his father? Data.', "After an unsuccessful harvest, why did the farmer decide to try a career in music? Because he had a ton of sick beets.", 'What do you call a Frenchman wearing sandals? Philippe Flop.', 'Which days are the strongest? Saturday and Sunday. The rest are weekdays.', "I just found out I’m colorblind. The news came out of the purple!", "What's the difference between a well-dressed man on a unicycle and a poorly-dressed man on a bicycle? Attire.","Of all the inventions of the last 100 years, the dry erase board has to be the most remarkable.", "In America, using the metric system can get you in legal trouble.", "In fact, if you sneer at any other method of measuring liquids, you may be held in contempt of quart.", "My hotel tried to charge me ten dollars extra for air conditioning. That wasn’t cool.", "What do you call a beehive without an exit? Unbelievable.", "If I ever find the doctor who screwed up my limb replacement surgery…I’ll kill him with my bear hands.", "Did you know that the first french fries weren’t cooked in France? They were cooked in Greece.", "It's easy to convince ladies not to eat Tide Pods, but harder to deter gents.", "I asked my date to meet me at the gym but she never showed up. I guess the two of us aren't going to work out.", "How do you find Will Smith in a snowstorm? You look for fresh prints.", "The difference between a numerator and a denominator is a short line. Only a fraction of people will understand this.", "I found a wooden shoe in my toilet today. It was clogged.", "I can't take my dog to the pond anymore because the ducks keep attacking him. That's what I get for buying a pure bread dog.", "To whoever stole my copy of Microsoft Office, I will find you. You have my Word.", "What’s Forrest Gump’s password? 1forrest1.", "I used to run a dating service for chickens. But I was struggling to make hens meet.", "If prisoners could take their own mug shots…They’d be called cellfies.", "Have you heard about those new corduroy pillows? They're making headlines.", "If a pig loses its voice…does it become disgruntled?", "What do you call a bundle of hay in a church? Christian Bale.", "A ship carrying red paint and a ship carrying blue paint collide in the middle of the ocean. Both crews were marooned.", "What is a guitar player's favorite Italian food? Strum-boli."]

@client.event
async def on_ready():
  print('bot is ready.')
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = f"{len(client.users)} users in {len(client.guilds)} servers〡!help"))

  



players = {}

memes = ['dankmemes', 'memes', 'meme']

swmemes = ['PrequelMemes', 'StarWarsMemes', 'OTMemes' 'SequelMemes']

reddit = praw.Reddit(client_id = "",
                    client_secret = "",
                    username = "",
                    password = '',
                    user_agent = "")

@client.command()
async def meme(ctx):
  subreddit = reddit.subreddit(random.choice(memes))
  all_subs = []
  top = subreddit.top(limit = random.randrange(1, 80))

  for submission in top:
    all_subs.append(submission)

  random_sub = random.choice(all_subs)

  name = random_sub.title
  url = random_sub.url

  em = discord.Embed(title = name, url = f"{random_sub.url}", color = (0x1abc9c))

  em.set_image(url = url)

  em.set_footer(text = f'👍{random_sub.score} | 💬 {random_sub.num_comments}')

  await ctx.send(embed = em)

@client.command()
async def uptime(ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=discord.Color.teal())
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text="Memetastic")
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)

@client.command()
async def google(ctx,*,search):
  await ctx.send(f'https://www.google.com/search?q={search}&oq=df&aqs=chrome..69i57j46i199i291i433i512j0i512j0i433i512j46i199i291i433i512j0i433i512j0i512j0i433i512j46i175i199i512j0i271.80833j0j7&sourceid=chrome&ie=UTF-8')

@client.command()
async def rps(ctx, user_choice):
    rpsGame = ['rock', 'paper', 'scissors']
    if user_choice.lower() in rpsGame: # Better use this, its easier. [lower to prevent the bot from checking a word like this "rOcK or pApeR"
        bot_choice = random.choice(rpsGame)
        embed = discord.Embed(title = f'{ctx.author.name} vs Memetastic', color = (0x1abc9c))
        embed.add_field(name = f"{ctx.author.name}'s choice", value = f'{user_choice}')
        embed.add_field(name = f"Memetastic's choice", value = f'{bot_choice}')
        await ctx.send(embed = embed)
        user_choice = user_choice.lower() # Also prevent a random word such as "rOcK"
        if user_choice == bot_choice:
            await ctx.send('We tied')
        # Rock Win Conditions #
        if user_choice == 'rock' and bot_choice == 'paper':
            await ctx.send('I won!')
        if user_choice == 'rock' and bot_choice == 'scissors':
            await ctx.send('You won!')
        # Paper Win Conditions #
        if user_choice == 'paper' and bot_choice == 'rock':
            await ctx.send('You won!')
        if user_choice == 'paper' and bot_choice == 'scissors':
            await ctx.send('I won!')
        # Scissor Win Conditions #
        if user_choice == 'scissors' and bot_choice == 'paper':
            await ctx.send('You won!')
        if user_choice == 'scissors' and bot_choice == 'rock':
            await ctx.send('I won!')
    else:
        await ctx.send('**Error** This command only works with rock, paper, or scissors.')
  
@client.command(description="Unmutes a specified user.")
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f" you have unmuted from: - {ctx.guild.name}")
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.teal())
   await ctx.send(embed=embed)

@client.command(description="Mutes the specified user.")
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted") 

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.teal())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")

@client.command()
async def discrim(ctx, member: discord.Member = None):
  if member == None:
    member = ctx.author
    await ctx.send(f'`#{member.discriminator}`')
  else:
    await ctx.send(f'`#{member.discriminator}`')

@client.event
async def on_message_delete(message):
    client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@client.command()
async def convo(ctx):
    msg = await ctx.channel.send("Yo! Are you going to invite me to your server?")
    await msg.add_reaction(u"\u2705")
    await ctx.message.add_reaction(u"\U0001F6AB")

    try:
        reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in [u"\u2705", u"\U0001F6AB"], timeout=30.0)


    except asyncio.TimeoutError:
        await ctx.channel.send("Ouch you ignored me.")

    else:
        if reaction.emoji == u"\u2705":
            await ctx.channel.send("You're an alpha male!")

        else:
            await ctx.channel.send("Ouch, that's just harsh...")    

snipe_message_author = {}
snipe_message_content = {}


@client.command()
async def minecraft(ctx, arg):
    r = requests.get('https://api.minehut.com/server/' + arg + '?byName=true')
    json_data = r.json()

    description = json_data["server"]["motd"]
    online = str(json_data["server"]["online"])
    playerCount = str(json_data["server"]["playerCount"])

    embed = discord.Embed(
        title=arg + " Server Info",
        description='Description: ' + description + '\nOnline: ' + online + '\nPlayers: ' + playerCount,
        color=discord.Color.dark_green()
    )
    embed.set_thumbnail(url="https://i1.wp.com/www.craftycreations.net/wp-content/uploads/2019/08/Grass-Block-e1566147655539.png?fit=500%2C500&ssl=1")

    await ctx.send(embed=embed)


@client.command()
async def dadjoke(ctx):
  await ctx.reply(random.choice(dj))

gifs = ['smile', 'meme', 'Weird']


@client.command()
async def gif(ctx,*,search):

  api_key = ''
  api_instance = giphy_client.DefaultApi()

  try:

    api_response = api_instance.gifs_search_get(api_key, search, limit= random.randrange(5, 80), rating='g')
    lst = list(api_response.data)
    giff = random.choice(lst)

    emb = discord.Embed(title=search, url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')
    emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')

    await ctx.send(embed=emb)

  except ApiException as e:
    print("Exception when calling")

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.command()
async def inspire(ctx):
  quote = get_quote()
  emb = discord.Embed(title="Inspiration", description = quote, color = discord.Colour.teal())
  await ctx.send(embed=emb)

@client.command(aliases=['8ball', '8b'])
async def eightball(ctx, *, question):
  responses=['Hell no.',
            'Prolly not.',
            'Idk bro.',
            'Prolly.',
            'Hell yeah my dude.',
            'It is certain.',
            'It is decidedly so.',
            'Without a Doubt.',
            'Yes - Definitaly.',
            'You may rely on it.',
            'As I see it, Yes.',
            'Most Likely.',
            'Outlook Good.',
            'Yes!',
            'No!',
            'Signs point to Yes!',
            'Better not tell you know.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't Count on it.",
            'My reply is No.',
            'My sources say No.',
            'Outlook not so good.',
            'Very Doubtful']
  await ctx.send(f':8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)}')

start_time = time.time()






@client.command()
async def wanted(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author


  wanted = Image.open("wanted.jpeg")

  asset = user.avatar_url_as(size = 128)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)

  pfp = pfp.resize((288,288))

  wanted.paste(pfp, (90,225))

  wanted.save("profile.jpeg")

  await ctx.send(file = discord.File("profile.jpeg"))




player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


@client.command()
async def hello(ctx):
  await ctx.send("hiya")

@client.command(pass_context=True)
async def randomnumber(ctx):
  embed = discord.Embed(title = "Random Number", description = (random.randint(1, 10000000)), color = (0x1abc9c))
  await ctx.send(embed = embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,member:discord.Member,*,reason=None):
    await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx,member:discord.Member,*,reason=None):
    await member.ban(reason=reason)

@client.command()
@commands.has_permissions(kick_members=True)
async def purge(ctx, amount=5):
  await ctx.channel.purge(limit=amount)

@client.command()
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()	
	member_name, member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		
		if (user.name, user.discriminator) == (member_name, member_discriminator):
 			await ctx.guild.unban(user)
 			await ctx.channel.send(f"Unbanned: {user.mention}")
       
mainshop = [{"name":"Watch","price":100,"description":"Time"},
            {"name":"Laptop","price":1000,"description":"Work"},
            {"name":"PC","price":10000,"description":"Gaming"},
            {"name":"ferrari","price":99999,"description":"Sports Car"},
            {"name":"Trump","price":696969, "description":"Donald Trump is for sale on Facebook Marketplace"},
            {"name":"Pinto","price":696969, "description":"Pinto is thiccc"}]

@client.command()
async def ping(ctx):
  await ctx.send(f":ping_pong: pong `{round(client.latency * 1000)}ms`")



@client.command()
async def userinfo(ctx, member : discord.Member):

  roles = member.roles[-1:0:-1]
  embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

  embed.set_author(name=member.name)
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(text=f'Requested by {ctx.author}',icon_url=ctx.author.avatar_url)

  embed.add_field(name="ID:", value=member.id)
  embed.add_field(name="Guild name:", value = member.display_name)

  embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
  embed.add_field(name = "Joined at:", value = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
  perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
  embed.add_field(name="Guild permissions", value=perm_string, inline=False)
  if member.status.name == "online":
    status = "Online :green_circle:"
  elif member.status.name == "offline":
    status = "Offline :black_circle:"
  elif member.status.name == "dnd":
    status = "Do Not Disturb :red_circle:"
  elif member.status.name == "streaming":
    status = "Streaming :purple_circle:"
  elif member.status.name == "idle":
    status = "Idle :yellow_circle:"

  embed.add_field(name = "Status:", value = status)
  embed.add_field(name = "System:", value = member.system)
  embed.add_field(name = "Is on Mobile:", value = member.mobile_status)
  embed.add_field(name = "Is on Web app:", value = member.web_status)
  embed.add_field(name = "DM Channel:", value = member.dm_channel)
  embed.add_field(name = "Default Avatar:", value = member.default_avatar)
  embed.add_field(name = "Pending?", value = member.pending)
  embed.add_field(name = "Nitr0:", value = member.premium_since)
  embed.add_field(name = "Relationship:", value = member.relationship)
  embed.add_field(name = "Is on Desktop:", value = member.desktop_status)
  embed.add_field(name = f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
  embed.add_field(name="Top Role:", value = member.top_role.mention)
  embed.add_field(name="Bot?", value = member.bot)
  await ctx.send(embed=embed)





@client.command()
async def spotify(ctx, user: discord.Member=None):
    user = user or ctx.author
    for activity in user.activities:
        if isinstance(activity, Spotify):
            embed = discord.Embed(title = "Spotify", description = f"{user.mention}", color = activity.color)
            embed.add_field(name = "Song:", value = f"{activity.title}")
            embed.add_field(name = "Artist:", value = f"{activity.artist}")
            embed.add_field(name = "Album", value = f"{activity.album}")
            embed.add_field(name = "Party ID:", value = f"{activity.party_id}")
            embed.add_field(name = "Track ID:", value = f"{activity.track_id}")
            embed.add_field(name="Started at:", value=activity.start.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(name="Will end at:", value=activity.end.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.set_thumbnail(url = activity.album_cover_url)
            await ctx.send(embed = embed)

@client.command()
async def emojify(ctx,*,text):
  emojis = []
  for s in text.lower():
    if s.isdecimal():
      num2emo = {'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine'}
      emojis.append(f':{num2emo.get(s)}:')
    elif s.isalpha():
      emojis.append(f':regional_indicator_{s}:')
    else:
      emojis.append(s)
  await ctx.send(' '.join(emojis))



@client.command(aliases=['bal'])
async def balance(ctx, *, user: discord.User = None):
    if user is None:
        user = ctx.author
    await open_account(user)

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f"{user.name}'s Balance", color = (0x1abc9c))
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance',value=bank_amt)
    await ctx.send(embed= em)

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    msg = '**Still on cooldown**, please try again in {:.2f}s'.format(error.retry_after)
    await ctx.send(msg)


@client.command()
@commands.cooldown(1,10,commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(101)

    await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)

@client.command()
@commands.cooldown(1,480,commands.BucketType.user)
async def work(ctx):
    await open_account(ctx.author)
    user = ctx.author

    jobs = ['Gamer', 'Fashion designer', 'Mechanic', 'Youtuber', 'delivery man', 'Police officer', 'engineer', 'Programmer', 'Tennis player', 'Doctor', 'Nurse', 'accountant', 'lawyer']

    users = await get_bank_data()

    earnings = random.randrange(500, 3000)

    await ctx.send(f'{ctx.author.mention} worked as a `{random.choice(jobs)}` and earnt {earnings} coins!!')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)


@client.command()
@commands.cooldown(1,86400,commands.BucketType.user)
async def daily(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = 150000

    embed = discord.Embed(title = "**Daily Coins**", description = f"Here are your {earnings} coins for the day!")

    await ctx.send(embed = embed)

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)



@client.command(aliases=['wd'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,'bank')
    await ctx.send(f'{ctx.author.mention} You withdrew {amount} coins')

@client.command(aliases=['dp'])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You deposited {amount} coins')


@client.command(aliases=['sm'])
@commands.cooldown(1,60,commands.BucketType.user)
async def send(ctx,member : discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount,'bank')
    await update_bank(member,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You gave {member.name} {amount} coins')


@client.command(aliases=['rb'])
@commands.cooldown(1,180,commands.BucketType.user)
async def rob(ctx,member : discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)


    if bal[0]<100:
        await ctx.send('It is useless to rob him :(')
        return

    earning = random.randrange(0,bal[0])

    await update_bank(ctx.author,earning)
    await update_bank(member,-1*earning)
    await ctx.send(f'{ctx.author.mention} You robbed {member.name} and got {earning} coins')


@client.command()
@commands.cooldown(1,180,commands.BucketType.user)
async def slots(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    final = []
    for i in range(3):
        a = random.choice(['X','O','Q'])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author,2*amount)
        await ctx.send(f'You won :) {ctx.author.mention}')
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send(f'You lose :( {ctx.author.mention}')


@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop", description = "The Shop", color = (0x1abc9c))

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)

@client.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def buy(ctx,item, amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag",  color = (0x1abc9c))
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)


async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]
  

@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 10):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = ":trophy: Leaderboard :trophy:",color = discord.Color(0x1abc9c))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}⏣",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.7* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('mainbank.json','w') as f:
        json.dump(users,f)

    return True


async def get_bank_data():
    with open('mainbank.json','r') as f:
        users = json.load(f)

    return users


async def update_bank(user,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
    return bal


@client.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def postmeme(ctx):

  responses = ['You posted a dank meme and made you', f'You posted a dead meme and the response was decent. You earned', f'You posted a pepe meme and you earned quite a bit of money which was', 'You posted a Freshhh meme and tiktok hated it and you made']

  await open_account(ctx.author)
  user = ctx.author

  users = await get_bank_data()

  earnings = random.randrange(200, 3000)

  await ctx.send(f'{random.choice(responses)} {earnings} coins')

  users[str(user.id)]["wallet"] += earnings

  with open("mainbank.json",'w') as f:
      json.dump(users,f)


      



@client.command()
async def help(ctx):
  user = ctx.author
  embed = discord.Embed(title = "The commands", color = (0x1abc9c))
  embed.add_field(name = "`!help_fun 😀`", value = 'Fun Commands', inline = False)
  embed.add_field(name = "`!help_moderation ⚖️`", value = 'Moderation Commands', inline = False)
  embed.add_field(name = "`!help_utility 🛠️`", value = 'Utility Commands', inline = False)
  embed.add_field(name = "`!help_games 🎲`", value = 'Game commands', inline = False)
  embed.add_field(name = "`!help_economy 💸`", value = 'Economy commands', inline = False)
  embed.add_field(name = "Upvote me!", value = "[`Click here`](https://top.gg/bot/843503749226037298/vote)")
  embed.add_field(name = "Invite me!", value = "[`Click here`](https://discord.com/oauth2/authorize?client_id=843503749226037298&permissions=0&scope=bot)")
  embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/843503749226037298/377c5cd760b12b4e836420461af0b224.png?size=128')

  await user.send(embed = embed)
  await ctx.send(f'{ctx.author.mention}, I have messaged My commands')

@client.command()
async def help_moderation(ctx):
  user = ctx.author
  embed = discord.Embed(title = "Moderation commands ⚖️", description = "Commands regarding moderation", color = (0x1abc9c))
  embed.add_field(name = "!purge", value = "Purges the number of messages place next to !purge (!purge 5)")
  embed.add_field(name = "!kick", value = "Kicks the user you mentioned next to !kick")
  embed.add_field(name = "!ban", value = "Bans the user you mention next to !ban")
  embed.add_field(name = "!unban", value = "unbans the user you put next to the command")
  embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/843503749226037298/377c5cd760b12b4e836420461af0b224.png?size=128')

  await user.send(embed = embed)
  await ctx.send(f'{ctx.author.mention}, I have messaged you the commands for moderation')

@client.command()
async def help_economy(ctx):
  user = ctx.author
  embed = discord.Embed(title = "Economy commands 💸", description = "Commands regarding economy", color = (0x1abc9c))
  embed.add_field(name = "!bag", value = "The items you have")
  embed.add_field(name = "!bal", value = "Shows the number of money you have in the wallet and in your bank")
  embed.add_field(name = "!slots", value = "Want a chance at winning money? Select the number of coins you wanna gamble by keeping it next to the command")
  embed.add_field(name = "!withdraw", value = "Removes a certain amount of money from your bank account and places it in your wallet")
  embed.add_field(name = "!deposit", value = "Puts a certain number of coins in your bank account from your wallet")
  embed.add_field(name = "!leaderboard", value = "The top 10 richest people across all of Memetastic!")
  embed.add_field(name = "!rob", value = "Rob Money from someone..... shhhh")
  embed.add_field(name = "!send", value = "be a good boy and send some money to someone")
  embed.add_field(name = "!buy", value = "After typing !buy make sure you put the product you want to buy and then the number which decides how many you have. e.g. !buy PC 100")
  embed.add_field(name = "!sell", value = "Sell an item from your bag")
  embed.add_field(name = "!shop", value = "The shop of Memetastic")
  embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/843503749226037298/377c5cd760b12b4e836420461af0b224.png?size=128')

  await user.send(embed = embed)
  await ctx.send(f'{ctx.author.mention}, I have messaged you the commands for the economy system')

@client.command()
async def help_utility(ctx):
  user = ctx.author
  embed = discord.Embed(title = "Utility commands 🛠️", description = "Commands regarding utility", color = (0x1abc9c))
  embed.add_field(name = "!serverinfo", value = "Provides information on the server")
  embed.add_field(name = "!userinfo", value = "proivides information on you or the user you mentioned")
  embed.add_field(name = "!poll", value = "Starts a poll based on the question you asked")
  embed.add_field(name = '!giveaway', value = 'Starts a giveaway and asks you a few questions regarding the details')

  embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/843503749226037298/377c5cd760b12b4e836420461af0b224.png?size=128')

  await user.send(embed = embed)
  await ctx.send(f'{ctx.author.mention}, I have messaged you the commands for utility')

@client.command()
async def help_fun(ctx):
  user = ctx.author
  embed = discord.Embed(title = "Fun commands 😀", description = "Commands regarding having fun", color = (0x1abc9c))
  embed.add_field(name = '!gif', value = 'A random gif based on your search', inline = True)
  embed.add_field(name = '!ping', value = 'The ping of the bot in ms', inline = True)
  embed.add_field(name = "!meme", value = "Gets a random meme from Reddit")
  embed.add_field(name = '!minecraft', value = 'After placing !minecraft make sure you add a server name to get the stats for that server!', inline = True)
  embed.add_field(name = '!revelation', value = 'Woah... a big reveal!', inline = True)
  embed.add_field(name = '!hello', value = 'Says Hiya', inline = True)
  embed.add_field(name = '!randomnumber', value = 'Gives you a random number', inline = True)
  embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/843503749226037298/377c5cd760b12b4e836420461af0b224.png?size=128')
  await user.send(embed = embed)
  await ctx.send(f'{ctx.author.mention}, I have messaged you the commands for in order to have fun')

@client.command()
async def help_games(ctx):
  user = ctx.author
  embed = discord.Embed(title = "Game commands 🎲", description = "Commands regarding games", color = (0x1abc9c))
  embed.add_field(name = '!tictactoe', value = 'After this command you have to @ your self and the person you want to play against. e.g. !tictactoe @user1 @user2', inline = True)
  embed.add_field(name = "!meme", value = "Gets a random meme from Reddit")
  embed.add_field(name = '!place', value = 'This is for the tictactoe command. You type !place and a number from 1 - 9 in order to place on the grid', inline = True)
  embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/843503749226037298/377c5cd760b12b4e836420461af0b224.png?size=128')

  await user.send(embed = embed)
  await ctx.send(f'{ctx.author.mention}, I have messaged you the commands for in order to have fun')
  
@client.command()
async def dm(ctx, member: discord.Member, *, msg):
  await member.send(f'{msg}: by {ctx.author.name}')
  await ctx.send(f"{msg} was sent to {member.member.mention}")

@client.command()
async def ticket(ctx, member: discord.Member, *, msg):
  await member.send(f'{msg}: by {ctx.author.mention}')
  await ctx.send(f"{msg} was sent to {member.name}")



  @client.command(name='serverinfo', aliases=['ServerInfo'])
  async def serverinfo(ctx):
    role_count = len(ctx.guild.roles)
    guild = ctx.message.guild
    embed = discord.Embed(
      color = discord.Color(0x1abc9c),
      title = f"{ctx.guild.name}"
    )
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    embed.add_field(name='Region', value=f"{ctx.guild.region}")
    embed.add_field(name='Owner', value=f"{ctx.guild.owner.mention}")
    embed.add_field(name ='Member count', value=f"{ctx.guild.member_count}")
    embed.add_field(name = "Guild description", value = guild.description, inline = True)
    embed.add_field(name = 'Guild verification level', value = guild.verification_level, inline = True)
    embed.add_field(name = 'Emoji Limit', value = ctx.guild.emoji_limit, inline = True)
    embed.add_field(name = 'Preferred Locale', value = ctx.guild.preferred_locale, inline = True)
    embed.add_field(name = 'Guild banner', value = guild.banner, inline = True)
    embed.add_field(name = 'Filesize Limit', value = f"{guild.filesize_limit} Bytes", inline = True)
    embed.add_field(name = 'Discovery Splash', value = guild.discovery_splash, inline = True)
    embed.add_field(name = "Guild Explicit content filter", value = guild.explicit_content_filter,inline = False)
    embed.add_field(name = "Guild boost count", value = guild.premium_subscription_count, inline = False)
    embed.add_field(name = "Number of roles", value =str(role_count), inline=False)
    embed.add_field(name = "Highest role", value =ctx.guild.roles[-1].mention, inline=False)
    embed.set_footer(icon_url=f"{ctx.guild.icon_url}", text = f"Guild ID: {ctx.guild.id}")
    await ctx.send(embed=embed)

@client.command()
async def suggest(ctx,*,suggestion):
  author=ctx.message.author
  file=open("suggestions.txt","a+")
  file.write(str(author)+" : "+suggestion+"\n")
  embed = discord.Embed(
    title = 'Suggestion',
    description = f"This Was Suggested By {ctx.author.mention}:\n {suggestion}",
    colour = (0x1abc9c)
  )
  channel = client.get_channel(123456789123456789)
  msg7 = await ctx.send(embed=embed)
  await msg7.add_reaction('👍')
  await msg7.add_reaction('👎')

@client.command()
async def revelation(ctx):
  await ctx.send("https://tenor.com/view/00-gif-21614373")

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

@client.command()
async def giveaway(ctx):
    await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

    questions = ["Which channel should it be hosted in?", 
                "What should be the duration of the giveaway? (s|m|h|d)",
                "What is the prize of the giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)

    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer. Please enter an integer next time")
        return            

    prize = answers[2]

    await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")


    embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = (0x1abc9c))

    embed.add_field(name = "Hosted by:", value = ctx.author.mention)

    embed.set_footer(text = f"Ends {answers[1]} from now!")

    my_msg = await channel.send(embed = embed)


    await my_msg.add_reaction("🎉")


    await asyncio.sleep(time)


    new_msg = await channel.fetch_message(my_msg.id)


    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! {winner.mention} won {prize}!")



    embed2 = discord.Embed(title = "Giveaway!", description = f"{prize}", color = (0x1abc9c))

    embed2.add_field(name = "Hosted by:", value = ctx.author.mention)

    embed2.add_field(name = "Winner:", value = winner.mention)

    embed2.set_footer(text = f"Giveaway ended")

    await my_msg.edit(embed = embed2)
    

@client.command()
async def avatar(ctx, member: discord.Member = None):
  if member == None:
    member = ctx.author

  memberAvatar = member.avatar_url

  ava_embed = discord.Embed(title = f"{member.name}'s avatar", color = (0x1abc9c))
  ava_embed.set_image(url = memberAvatar)

  await ctx.send(embed = ava_embed)

@client.command()
async def poll(ctx,*,message):
    emb=discord.Embed(title=" POLL 📢", description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')


@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
                    
@client.command()
async def reactrole(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)

@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

@client.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
@commands.bot_has_permissions(attach_files = True, embed_links = True)
async def reminder(ctx, time, *, reminder):
    print(time)
    print(reminder)
    user = ctx.author
    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
    embed.set_footer(text="If you have any questions, suggestions or bug reports, please join our support Discord Server: link hidden", icon_url=f"{client.user.avatar_url}")
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration, send `reminder_help` for more information.')
    elif seconds < 300:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
        await asyncio.sleep(seconds)
        await ctx.send(f"Hi, you asked me to remind you about {reminder} {counter} ago.")
        return
    await ctx.send(embed=embed)

@client.command()
async def define(ctx, word):
  response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en_US/{word}')
  if response.status_code == 404:
    await ctx.send('Word not found')
    return
  else:
    wordx = response.json()
    the_dictionary = wordx[0]
    meanings = the_dictionary['meanings']
    definitions = meanings[0]
    definition = definitions['definitions']
    meaningg = definition[0]
    meaning = meaningg['definition']
    example = meaningg.get('example', 'None')
    synonymslist = meaningg.get('synonyms', 'None')
    if isinstance(synonymslist, str):
      synonymslist = [synonymslist]
    synonyms = ', '.join(synonymslist)
    deffinal = discord.Embed(title = f"`{word}`")
    deffinal.add_field(name = 'Definition', value = f"{meaning}")
    deffinal.add_field(name = "Example", value = f'{example}')
    deffinal.add_field(name = "Synonyms", value = f"{synonyms}")
    await ctx.send(embed=deffinal)

@client.command() 
async def add(ctx,a:int,b:int): 
    await ctx.send(f"{a} + {b} = {a+b}") #Adds A and B

@client.command() 
async def sub(ctx,a:int,b:int): 
    await ctx.send(f"{a} - {b} = {a-b}") #Subtracts A and B

@client.command() 
async def multiply(ctx,a:int,b:int): 
    await ctx.send(f"{a} * {b} = {a*b}") #Multplies A and B

@client.command() 
async def divide(ctx,a:int,b:int): 
    await ctx.send(f"{a} / {b} = {a/b}") #Divides A and B

@client.command()
async def calculate(ctx, operation, *nums):
    if operation not in ['+', '-', '*', '/']:
        await ctx.send('Please type a valid operation type.')
    var = f' {operation} '.join(nums)
    await ctx.send(f'{var} = {eval(var)}')

@client.command()
async def embed(ctx):

    questions = ["Which should be the tile of the embed?",
            "What should be the description?",
            "What is the color of the embed? This should be a hex color.", "What should the image of the embed be?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)


    embedcolor = answers[2]
    img = answers[3]

    embed = discord.Embed(description=answers[1], title=answers[0], colour=int(embedcolor, 16))
    embed.set_image(url = answers[3])

    await ctx.send(embed=embed)

@client.command()
async def say(ctx, channel:discord.TextChannel,* , message):    
    await channel.send(message)
    await ctx.message.delete()

@client.command()
async def world(ctx):
    embed = discord.Embed(
        title = "COVID-19 Global Satistics",
        colour = ctx.author.colour
    )
    api = requests.get("https://covid19.mathdro.id/api").json()
    confirmedCases = api["confirmed"]["value"]
    recoveredCases = api["recovered"]["value"]
    deaths = api["deaths"]["value"]
    embed.add_field(name = "Infected People", value = confirmedCases)
    embed.add_field(name = "People Recovered", value = recoveredCases)
    embed.add_field(name = "Deaths", value = deaths)
    embed.set_image(url = "https://covid19.mathdro.id/api/og")
    await ctx.send(embed = embed)

@client.command() 
async def country(ctx, country):
    embed = discord.Embed(
        title = f"COVID-19 Satistics for {country}",
        colour = ctx.author.colour
    )
    api = requests.get(f"https://covid19.mathdro.id/api/countries/{country}").json()
    confirmedCases = api["confirmed"]["value"]
    recoveredCases = api["recovered"]["value"]
    deaths = api["deaths"]["value"]
    embed.add_field(name = "Infected People", value = confirmedCases)
    embed.add_field(name = "People Recovered", value = recoveredCases)
    embed.add_field(name = "Deaths", value = deaths)
    embed.set_image(url = f"https://covid19.mathdro.id/api/countries/{country}/og")
    await ctx.send(embed = embed)

@client.command()
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
    await ctx.send( ctx.channel.mention + " ***is now in lockdown.***")

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked.***")

@client.command()
async def mock(ctx, *, message):
    out = ''.join(random.choice((str.upper, str.lower))(c) for c in message)
    await ctx.send(out)

@client.command()
async def invite(ctx):
  await ctx.send('https://dsc.gg/memetastic')

@client.command()
async def vote(ctx):
  await ctx.send('https://top.gg/bot/843503749226037298/vote')

@client.event
async def on_member_join(member):
  print(f"{member} has joined the server")
  with open('afk.json', 'r') as f:
    afk = json.load(f)

  await update_data(afk, member)

  with open('afk.json', 'w') as f:
    json.dump(afk, f)


async def update_data(afk, user):
  if not f'{user.id}' in afk:
    afk[f'{user.id}'] = {}
    afk[f'{user.id}']['AFK'] = 'False'

@client.event
async def on_message(message):
  with open('afk.json', 'r') as f:
    afk = json.load(f)

  for x in message.mentions:
    if afk[f'{x.id}']['AFK'] == 'True':
      if message.author.bot:
        return
      await message.channel.send(f'{x.name} is AFK')


  if not message.author.bot:
    await update_data(afk, message.author)


    if afk[f'{message.author.id}']['AFK'] == 'True':
      await message.channel.send(f'{message.author.mention} is No Longer AFK')
      afk[f'{message.author.id}']['AFK'] = 'False'
      with open('afk.json', 'w') as f:
        json.dump(afk, f)
      await message.author.edit(nick=f'{message.author.display_name[5:]}')


  with open('afk.json', 'w') as f:
    json.dump(afk, f)

  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
  pre = prefixes[str(message.guild.id)] 


  try:
      if message.mentions[0] == client.user:

          with open("prefixes.json", "r") as f:
              prefixes = json.load(f)

          pre = prefixes[str(message.guild.id)] 

          await message.channel.send(f"My prefix for this server is {pre}")

  except:
    pass

  await client.process_commands(message)


@client.command()
async def afk(ctx,*,reason = None):
  with open('afk.json', 'r') as f:
    afk = json.load(f)

  if not reason:
    reason = 'None'

  afk[f'{ctx.author.id}']['AFK'] = 'True'
  await ctx.send(f'You are now AFK. Reason: {reason}')
  with open('afk.json', 'w') as f:
    json.dump(afk, f)


  await ctx.author.edit(nick=f'[AFK] {ctx.author.display_name}')




@client.command()
async def defaultavatar(ctx, member: discord.Member = None):
  if member == None:
    member = ctx.author

  memberAvatar = member.default_avatar_url

  ava_embed = discord.Embed(title = f"{member.name}'s  defaultavatar", color = (0x1abc9c))
  ava_embed.set_image(url = memberAvatar)

  await ctx.send(embed = ava_embed)

@client.command()
async def track(ctx, user: discord.Member = None):
  user = user or ctx.author
  spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

  if spotify_result is None:
    await ctx.send(f'{user.name} is not listening to spotify')

  track_background_image = Image.open("spotify_template.png")
  album_image = Image.open(requests.get(spotify_result.album_cover_url, stream = True).raw).convert('RGBA')

  title_font = ImageFont.truetype('theboldfont.ttf', 16)
  artist_font = ImageFont.truetype('theboldfont.ttf', 14)
  album_font = ImageFont.truetype('theboldfont.ttf', 14)
  start_duration_font = ImageFont.truetype('theboldfont.ttf', 12)
  end_duration_font = ImageFont.truetype('theboldfont.ttf', 12)


  title_text_position = 150, 30
  artist_text_position = 150, 60
  album_text_position = 150, 80
  start_duration_text_position = 150, 122
  end_duration_text_position = 515, 122

  draw_on_image = ImageDraw.Draw(track_background_image)
  draw_on_image.text(title_text_position, spotify_result.title, 'white', font=title_font)
  draw_on_image.text(artist_text_position, f'by {spotify_result.artist}', 'white', font=artist_font)
  draw_on_image.text(album_text_position, spotify_result.album, 'white', font=album_font)
  draw_on_image.text(start_duration_text_position, '0:00', 'white', font=start_duration_font)
  draw_on_image.text(end_duration_text_position,f"{dateutil.parser.parse(str(spotify_result.duration)).strftime('%M:%S')}",'white', font=end_duration_font)


  album_color = album_image.getpixel((250, 100))
  background_image_color = Image.new('RGBA', track_background_image.size, album_color)
  background_image_color.paste(track_background_image, (0, 0), track_background_image)

  album_image_resize = album_image.resize((140, 160))
  background_image_color.paste(album_image_resize, (0, 0), album_image_resize)

  f = background_image_color.convert('RGB').save('spotify.jpg', 'JPEG',  dpi=(400, 400))



  await ctx.send(file=discord.File('spotify.jpg'))




keep_alive()
client.run(TOKEN)

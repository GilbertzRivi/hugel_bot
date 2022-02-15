import discord, io, random, os
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.commands import Greedy



load_dotenv('bot/.env')
responces =  ['^w^\nAwwww jakie to slodkie!', '\nAwwww ^w^', 'OwO', 'Slodko x3', 'ale slodziaki uwu', 'UwU', '<:serduszko:553730684368453633>', 'dawww >/w/< slodziaki']

client = commands.Bot(command_prefix="-", fetch_offline_members=True, intents=discord.Intents().all())
client.remove_command('help')
client.url_conv_channel = ''
client.doesnt_like_roles = [598083613946544128, 670315076183523329, 670315080948383770, 670315084089786368, 670315087164342292, 683329688944246819, 670315758479343676]
client.guild = 524355460313120778

def read_b(file_path: str) -> bytes:
    with open(file_path, 'rb') as f:
        return f.read()

def discord_file(path: str, name: str, spoiler: bool = False) -> discord.File:
    return discord.File(io.BytesIO(read_b(path)), filename=name, spoiler=spoiler)

def get_image(folder: str) -> discord.File:
    image_path = random.choice(os.listdir(folder))
    image_path = f'{folder}/{image_path}'
    image = discord_file(image_path, image_path)
    return image

async def command_processing(ctx, members: list, type: str) -> None:

    #creating variables
    if type == 'hug':
        self_response = 'przytulić'
        doesnt_like = 'tulano'
        footer_text = 'tulajo'
        embed_name = 'Hugi!'
        embed_text = 'tula'
        folder = './bot/hugs'
    elif type == 'kiss':
        self_response = 'pocałować'
        doesnt_like = 'całowano'
        footer_text = 'całujo'
        embed_name = 'Kissy!'
        embed_text = 'całuje'
        folder = './bot/kisses'
    elif type == 'boop':
        self_response = 'boopnąć'
        doesnt_like = 'boopano'
        footer_text = 'boopajo'
        embed_name = 'Boopy!'
        embed_text = 'boopa'
        folder = './bot/boops'
    elif type == 'pat':
        self_response = 'patnąć'
        doesnt_like = 'patano'
        footer_text = 'patajo'
        embed_name = 'Paty!'
        embed_text = 'pata'
        folder = './bot/pats'
    elif type == 'lick':
        self_response = 'polizać'
        doesnt_like = 'lizano'
        footer_text = 'lizajo'
        embed_name = 'Lizy!'
        embed_text = 'liza'
        folder = './bot/licks'
    elif type == 'nom':
        self_response = 'nomnąć'
        doesnt_like = 'nomano'
        footer_text = 'nomajo'
        embed_name = 'Nomy!'
        embed_text = 'noma'
        folder = './bot/noms'

    #checking if person is not huging themself
    if ctx.author in members:
        image_file = discord_file(".bot/beyond science.png", ".bot/beyond science.png")
        await ctx.send(f"Ej <@{ctx.author.id}>\nNie mozesz {self_response} samego siebie <:thonk:531349115041480715>", file=image_file)
        return False

    #removing people that doesn't like hugs from members list
    for member in members:
        for role in member.roles:
            if role in client.doesnt_like_roles:
                members.remove(member)
 
    if len(members) == 0:
        await ctx.send(f'Niestety ta osoba nie życzy sobie aby ją {doesnt_like} :/')
        return False

    #editing message instead of posting a new one if hug/pat etc is an responce
    async for message in ctx.channel.history(limit=50):
        if message.author == client.user and len(message.embeds) > 0:
            
            embed = message.embeds[0]
            if embed_text in embed.fields[0].value.split(' '):
            
                temp_members = []
                for elem in embed.fields[0].value.split(' '):
                    
                    #extracting members from embed
                    try:
                        temp_members.append(ctx.message.guild.get_member(int(elem[2:-1])))
                    except ValueError:
                        try:
                            temp_members.append(ctx.message.guild.get_member(int(elem[3:-1])))
                        except: pass

                #editing embed
                if len(temp_members) == 2:
                    image = get_image(folder)
                    temp = await client.url_conv_channel.send(file=image)
                    image_url = temp.attachments[0].url

                    embed.set_image(url=image_url)
                    embed.set_field_at(0, name = embed_name, value = f'{temp_members[0].mention} i {temp_members[1].mention} {footer_text} się nawzajem :3')
                    await message.edit(embed=embed)
                    return
            break

    #getting an image for hug
    image = get_image(folder)
    temp = await client.url_conv_channel.send(file=image)
    image_url = temp.attachments[0].url

    embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)

    if random.randint(1,35) == 1:
        embed.set_footer(text='pedalo sie uwu', icon_url=ctx.author.avatar_url)
    else:
        embed.set_footer(text=f'{footer_text} sie uwu', icon_url=ctx.author.avatar_url)
    
    embed.set_image(url=image_url)
    
    #setting up embed with proper text
    if client.user.id in [member.id for member in members]:
        if len(members) == 1:
            embed.add_field(name=embed_name, value=f'{ctx.author.mention} mnie {embed_text} >w<\nDziekuje!')
        else:
            members.remove(client.user)
            mentions = ' '.join([member.mention for member in members])
            embed.add_field(name=embed_name, value=f"{ctx.author.mention} {embed_text} {mentions} i mnie >w<\nDziekuje!")
    else:
        mentions = ' '.join([member.mention for member in members])
        comment = random.choice(responces)
        embed.add_field(name=embed_name, value=f"{ctx.author.mention} {embed_text} {mentions} {comment}")

    #sending message and adding reaction
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(emoji='➡️')
    
    #deleting old messages
    temp = 0
    async for message in ctx.channel.history(limit=50):
        if message.author == client.user and len(message.embeds) == 1:
            temp += 1
            if temp > 5:
                await message.delete()



@client.event                                                           #on ready 
async def on_ready():
    print(f"Zalogowano jako {client.user.name}")
    await client.change_presence(activity=discord.Game(name='-hug @osoba'))
    client.url_conv_channel = client.get_channel(670275562945773599)
    client.guild = client.get_guild(524355460313120778)
    client.doesnt_like_roles = [client.guild.get_role(id) for id in client.doesnt_like_roles]

@client.event                                                           #message edit
async def on_message_edit(_, after):
    await client.process_commands(after)

@client.event                                                           #przewijanie
async def on_reaction_add(reaction, user):
    if reaction.message.author != client.user or reaction.emoji != "➡️" or user == client.user:
        return

    message = reaction.message
    embed = message.embeds[0]
    field = embed.fields[0].value
    
    members = []
    for elem in field.split(' '):
        try:
            members.append(reaction.message.guild.get_member(int(elem[2:-1])))
        except ValueError:
            try:
                members.append(reaction.message.guild.get_member(int(elem[3:-1])))
            except: pass

    await reaction.remove(user)
    if not user in members:
        return

    if 'tula' in field or 'tulają' in field:
        folder = './bot/hugs'
    elif 'całuje' in field or 'całują' in field:
        folder = './bot/kisses'
    elif 'boopa' in field or 'boopają' in field:
        folder = './bot/boops'
    elif 'pata' in field or 'patają' in field:
        folder = './bot/pats'
    elif 'liza' in field or 'lizają' in field:
        folder = './bot/licks'
    elif 'noma' in field or 'nomają' in field:
        folder = './bot/noms'
    
    image = get_image(folder)
    temp = await client.url_conv_channel.send(file=image)
    image_url = temp.attachments[0].url

    embed.set_image(url=image_url)
    await message.edit(embed=embed)

@client.command()                                                       #hug 
async def hug(ctx, members: Greedy[discord.Member]):

    await ctx.message.delete()
    
    members = list(set(members))
    if len(members) > 7:
        await ctx.send('Nie przesadzaj')
        return
    
    await command_processing(ctx, members, 'hug')

@client.command()                                                       #kiss
async def kiss(ctx, members: Greedy[discord.Member]):

    await ctx.message.delete()
    
    members = list(set(members))
    if len(members) > 7:
        await ctx.send('Nie przesadzaj')
        return
    
    await command_processing(ctx, members, 'kiss')
    
@client.command()                                                       #boop
async def boop(ctx, members: Greedy[discord.Member]):

    await ctx.message.delete()
    
    members = list(set(members))
    if len(members) > 7:
        await ctx.send('Nie przesadzaj')
        return
    
    await command_processing(ctx, members, 'boop')
    
@client.command()                                                       #pat
async def pat(ctx, members: Greedy[discord.Member]):

    await ctx.message.delete()
    
    members = list(set(members))
    if len(members) > 7:
        await ctx.send('Nie przesadzaj')
        return
    
    await command_processing(ctx, members, 'pat')
    
@client.command()                                                       #lick
async def lick(ctx, members: Greedy[discord.Member]):

    await ctx.message.delete()
    
    members = list(set(members))
    if len(members) > 7:
        await ctx.send('Nie przesadzaj')
        return
    
    await command_processing(ctx, members, 'lick')
    
@client.command()                                                       #nom
async def nom(ctx, members: Greedy[discord.Member]):

    await ctx.message.delete()
    
    members = list(set(members))
    if len(members) > 7:
        await ctx.send('Nie przesadzaj')
        return
    
    await command_processing(ctx, members, 'nom')

@client.command()
async def yiff(ctx):
    
    await ctx.message.delete()

    image = discord_file('./bot/nohorny.jpg', 'nohorny.jpg')

    await ctx.send(file=image)

client.run(os.getenv('TOKEN'))

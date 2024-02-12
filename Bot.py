import discord 
from discord.ext import commands, tasks
import datetime
import discord.ui
from discord.ui import View, Button, Select
import random
from datetime import datetime, timedelta
import asyncio


intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command("help")


@bot.event
async def on_ready():
    print("The bot is now online")

@bot.command()
async def hello(ctx):
    """
    Fai un saluto al bot!
    """
    username = ctx.message.author.name
    await ctx.send("Hii " + username)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner", "Pagato Normalmente", "I sottopagati")
async def ban(ctx, member:discord.Member, *,reason=None):
    """
    Ban di un utente (mod only)
    """
    if reason == None:
        reason = "This user was banned by " + ctx.message.author.name
    await member.ban(reason=reason)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner", "Pagato Normalmente", "I sottopagati")
async def kick(ctx, member:discord.Member, *,reason=None):
    """
    Kick di un utente (mod only)
    """
    if reason == None:
        reason = "This user was kicked by " + ctx.message.author.name
    await member.kick(reason=reason)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner", "Pagato Normalmente", "I sottopagati")
async def mute(ctx, member:discord.Member, timelimit):
    """
    Mute di un utente (mod only)
    """
    if "s" in timelimit:
        gettime = timelimit.strip("s")
        if int(gettime) > 2419000:
            await ctx.send("The time ammount cannot be bigger than 28days")
        else:
            newtime = datetime.timedelta(seconds=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    elif "m" in timelimit:
        gettime = timelimit.strip("m")
        if int(gettime) > 40320:
            await ctx.send("The time ammount cannot be bigger than 28days")
        else:
            newtime = datetime.timedelta(minutes=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    elif "h" in timelimit:
        gettime = timelimit.strip("h")
        if int(gettime) > 672:
            await ctx.send("The time ammount cannot be bigger than 28days")
        else:
            newtime = datetime.timedelta(hours=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    elif "d" in timelimit:
        gettime = timelimit.strip("d")
        if int(gettime) > 28:
            await ctx.send("The time ammount cannot be bigger than 28days")
        else:
            newtime = datetime.timedelta(days=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    elif "w" in timelimit:
        gettime = timelimit.strip("w")
        if int(gettime) > 4:
            await ctx.send("The time ammount cannot be bigger than 28days")
        else:
            newtime = datetime.timedelta(weeks=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner", "Pagato Normalmente", "I sottopagati")
async def unmute(ctx, member:discord.Member):
    """
    Unmute di un utente (mod only)
    """
    await member.edit(timed_out_until=None)

async def ticketcallback(interaction):
    guild = interaction.guild
    role = discord.utils.get(guild.roles, name="Moderator")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False), 
        interaction.user: discord.PermissionOverwrite(view_channel=True), 
        role: discord.PermissionOverwrite(view_channel=True),
    }

    select  = Select(options=[
        discord.SelectOption(label="Help Ticket", value="01", emoji="✔️", description="This will open a help ticket"),
        discord.SelectOption(label="Other Ticket", value="02", emoji="❌", description="This will open a ticket in the other section")
    ])

    async def my_callback(interaction):
        if select.values[0] == "01":
            category = discord.utils.get(guild.categories, name="Tickets")
            channel = await guild.create_text_channel(f"{interaction.user.name}+ticket", category=category, overwrites=overwrites)
            await interaction.response.send_message(f"Created ticket - <#{channel.id}")
            await channel.send("Hello, how I help?")
        elif select.values[0] == "01":
            category = discord.utils.get(guild.categories, name="Tickets")
            channel = await guild.create_text_channel(f"{interaction.user.name}-ticket", category=category, overwrites=overwrites)
            await interaction.response.send_message(f"Created ticket - <#{channel.id}")
            await channel.send("Hello, write your problem and a mod will respond to you!")

    select.callback = my_callback
    view = View(timeout=None)
    view.add_item(select)
    await interaction.response.send_message("Choose an option below", view=view, ephemeral=True)

@bot.command()
async def ticket(ctx):
    """
    Apri un ticket con i moderatori del server per parlare con loro
    """

    button = Button(label="Create Ticket", style=discord.ButtonStyle.green)
    button.callback = ticketcallback
    view = View(timeout=None)
    view.add_item(button)
    await ctx.send("Open a ticket below", view=view)

@bot.command()
async def cancelTicket(ctx):
    """
    Cancella un ticket già aperto
    """
    username = ctx.message.author.name + "ticket"
    existChannel = discord.utils.get(ctx.guild.channels, name=username)
    if existChannel:
        await existChannel.delete()
    else:
        await ctx.send(f'No channel named, "{username}", was found')

@bot.command()
async def roulette(ctx):
    """
    Roulette russa (scopri tu cosa succede se perdi ;) )
    """
    number = random.randint(1, 6)
    if(number == 3):
        await ctx.author.kick(reason="roulette")
        await ctx.send("He lost, what a loser")
    else:
        await ctx.send("You are safe .... this time")
        
@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner", "Pagato Normalmente", "I sottopagati")
async def cancella(ctx, numero_messaggi: int):
    """
    Cancella un certo numero di messaggi nella chat (mod only)
    """
    try:
        
        #bisogna usare sta schifezza perché sennò async_generator da errore di tipo flatten
        messaggi = []
        async for message in ctx.channel.history(limit=numero_messaggi + 1):
            messaggi.append(message)

        await ctx.channel.delete_messages(messaggi)


        # Invia un messaggio confermando l'operazione
        await ctx.send(f'Cancellati gli ultimi {numero_messaggi} messaggi.')
    except discord.Forbidden:
        await ctx.send("Non ho i permessi necessari per cancellare messaggi.")
    except discord.HTTPException as e:
        await ctx.send(f"Errore durante la cancellazione dei messaggi: {e}")

@bot.command(name='help')
async def help_command(ctx):
    """
    Mostra la lista dei comandi disponibili.
    """
    embed = discord.Embed(title='Comandi del Bot', description='Ecco la lista dei comandi disponibili:', color=0x9400D3)
    
    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)

    await ctx.send(embed=embed)
    
# Insert your key here to let the bot work 
bot.run('MTIwMDAyOTQ5NDU5Mzk4MjQ2NA.GW6YOD.01Z-3KhEr-O17kDMlniWJdIZ3LLWgZn6Eru9k8')
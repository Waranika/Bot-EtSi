import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from taskmanager import TaskManager

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/',intents=intents)  # Set the command prefix

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    if guild:
        print(f'{bot.user} has connected to {guild.name}!')
        channel = guild.get_channel(int(CHANNEL_ID))
        if channel:
            await channel.send('Hello!')
        else:
            print(f"Channel with ID {CHANNEL_ID} not found.")
    else:
        print(f"Guild with name {GUILD} not found.")
        
@bot.command(name='tasks')
async def display_tasks(ctx):
    task_manager = TaskManager()
    tasks = task_manager.get_tasks()
    task_manager.close_connection()

    if tasks:
        task_list = ""
        for task in tasks:
            task_list += f"\n{'✅' if task[4] == 1 else ':clock4:'} **{task[1]}**: {task[2]}. *Members: {task[3]}* \n"
        await ctx.send(f'__**Tasks Translator Afro Project**__ : {task_list}')
    else:
        await ctx.send('No tasks found.')

@bot.command(name='role')
async def assign_role(ctx, role_name):
    # Checking if the role exists in the guild
    member = ctx.message.author
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        # Assigning the role to the user
        await bot.add_roles(member, role)
        await ctx.send(f'The role {role_name} has been assigned to {ctx.author.mention}!')
    else:
        await ctx.send(f'The role {role_name} was not found.')


bot.run(TOKEN)

import os
from discord.ext import commands
from dislash import InteractionClient, SelectMenu, SelectOption, MessageInteraction
import discord
from dotenv import load_dotenv
from taskmanager import TaskManager

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)
# test_guilds param is optional, this is a list of guild IDs
inter_client = InteractionClient(bot, test_guilds=[DISCORD_GUILD_ID])
role_option=[]

@bot.event
async def on_ready():
    global role_option
    guild = bot.get_guild(DISCORD_GUILD_ID)
    if guild:
        print(f'{bot.user} has connected to {guild.name}!')
        
        # Exclude @everyone role
        role_names = [role.name for role in guild.roles if role.name != "@everyone"]
        
        print("Registered roles:")
        for role_name in role_names:
            print(role_name)
            role= SelectOption(role_name,role_name)
            role_option.append(role)
    else:
        print(f"Guild with ID {DISCORD_GUILD_ID} not found.")

@inter_client.slash_command(description="Says Hello")
async def hello(ctx):
    await ctx.send("Hello!")

@inter_client.slash_command(name='tasks',description="displays to-do tasks")
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

@inter_client.slash_command(name="role",description="choose a role")
async def role(ctx):
    global role_option
    await ctx.send(
        "Choose a role!",
        components=[
            SelectMenu(
                custom_id="test",
                placeholder="Choose a role",
                max_values=1,
                options=role_option
            )
        ]
    )
    
    @bot.event
    async def on_dropdown(inter: MessageInteraction):
        labels = [option.label for option in inter.select_menu.selected_options]
        print(labels)
        role_name=labels[0]
        member = ctx.author
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            # Assigning the role to the user
            await member.add_roles(role)
            await ctx.send(f'The role {role_name} has been assigned to {ctx.author.mention}!')
        else:
            await ctx.send(f'The role {role_name} was not found.')

bot.run(TOKEN)
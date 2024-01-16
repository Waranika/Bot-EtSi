import os
from discord.ext import commands
from dislash import InteractionClient, ActionRow, Button, ButtonStyle, SelectOption, MessageInteraction
import discord
from random import randint
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
            #print(role_name)
            role= SelectOption(role_name,role_name)
            role_option.append(role)
    else:
        print(f"Guild with ID {DISCORD_GUILD_ID} not found.")

@inter_client.slash_command(name="project_in_progress",description="shows details of current project")
async def project_in_progress(ctx):
    with open(r"Discord bot\translator_afro.txt", "r", encoding="utf-8") as file:
        project_details = file.read()

    await ctx.send(project_details)
    
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

@inter_client.slash_command(name="role",description="adds you to the ongoing project")
async def role(ctx):
    member = ctx.author
    role = discord.utils.get(ctx.guild.roles, name="AAT")
    if role:
        # Assigning the role to the user
        await member.add_roles(role)
        await ctx.send(f':confetti_ball: The role "AAT" has been assigned to {ctx.author.mention}!:confetti_ball:')
    else:
        await ctx.send(f'The role "AAT" was not found.')

@inter_client.slash_command(description="be added to a task in the current project")
async def be_add_to_a_task(ctx):
    task_manager = TaskManager()
    tasks = task_manager.get_tasks()
    task_manager.close_connection()
    rows=[]
    buttons=[]
    # Split the tasks into chunks of 5
    chunk_size = 5
    task_chunks = [tasks[i:i + chunk_size] for i in range(0, len(tasks), chunk_size)]
    color=[ButtonStyle.green,ButtonStyle.blurple]

    # Create buttons for each task
    buttons = [
        [
            Button(
                style=color[randint(0,1)],
                label=task[1],
                custom_id=str(task[0])
            )
            for task in task_chunk
        ]
        for task_chunk in task_chunks
    ]

    # Create ActionRows from buttons
    rows = [ActionRow(*button_chunk) for button_chunk in buttons]
        
        
    msg = await ctx.send("Choose a task you want to work on!", components=rows)

    # Here timeout=20 means that the listener will
    # finish working after 20 seconds of inactivity
    on_click = msg.create_click_listener(timeout=20) # doesn't work
    
    @on_click.matching_id("0")
    async def on_test_button_0(inter):
        await handle_task_selection(inter, "Selecting a Pre-trained Model", "Selecting a Pre-trained Model")

    @on_click.matching_id("1")
    async def on_test_button_1(inter):
        await handle_task_selection(inter, "Data Preparation", "Data Preparation")

    @on_click.matching_id("2")
    async def on_test_button_2(inter):
        await handle_task_selection(inter, "Fine-tuning", "Fine-tuning")

    @on_click.matching_id("3")
    async def on_test_button_3(inter):
        await handle_task_selection(inter, "Hyperparameter Tuning", "Hyperparameter Tuning")

    @on_click.matching_id("4")
    async def on_test_button_4(inter):
        await handle_task_selection(inter, "Evaluation", "Evaluation")

    @on_click.matching_id("5")
    async def on_test_button_5(inter):
        await handle_task_selection(inter, "Website (frontEnd)", "Website (frontEnd)")

    @on_click.matching_id("6")
    async def on_test_button_6(inter):
        await handle_task_selection(inter, "Website (BackEnd)", "Website (BackEnd)")

    async def handle_task_selection(inter, task_name, task_display_name):
        member = ctx.author
        pseudo = member.nick
        task_manager = TaskManager()
        
        check = task_manager.check_member(task=task_display_name, member=pseudo)
        print(f"the result was {check} for the user {pseudo}")
        if check:
            task_manager.be_member(task=task_display_name, member=pseudo)
            await inter.reply(f":loudspeaker: You've chosen the task **{task_name}**!")
            await msg.delete()
            task_manager.close_connection()
        else:
            await inter.reply(f":loudspeaker: You're already a member of the task **{task_name}**!")
            await msg.delete()
            task_manager.close_connection()

bot.run(TOKEN)
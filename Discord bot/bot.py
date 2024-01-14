import os
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    if guild:
        print(f'{client.user} has connected to {guild.name}!')
        channel = guild.get_channel(int(CHANNEL_ID)) # type: ignore
        if channel:
            await channel.send('Bonjour!') # type: ignore
        else:
            print(f"Channel with ID {CHANNEL_ID} not found.")
    else:
        print(f"Guild with name {GUILD} not found.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    if message.content.startswith('/create_role'):
        # Extracting the role name from the message
        _, role_name = message.content.split(" ", 1)

        # Creating the role in the guild
        try:
            role_color = discord.Color(random.randint(0, 0xFFFFFF))  # Random color
            role = await message.guild.create_role(
                name=role_name,
                color=role_color,
                permissions=discord.Permissions(1072705297985)  # Setting permissions
            )

            # Creating a category for the channels
            category = await message.guild.create_category(role_name)

            # Creating a private text channel with the same name as the role
            text_channel = await category.create_text_channel(role_name)

            # Overwriting permissions for the text channel
            for existing_role in message.guild.roles:
                await text_channel.set_permissions(existing_role, read_messages=False, send_messages=False)
            
            # Explicitly deny read_messages for the default role
            await text_channel.set_permissions(message.guild.default_role, read_messages=False)
            
            await text_channel.set_permissions(role, read_messages=True, send_messages=True)

            # Creating a private voice channel with the same name as the role
            voice_channel = await category.create_voice_channel(role_name)

            # Overwriting permissions for the voice channel
            for existing_role in message.guild.roles:
                await voice_channel.set_permissions(existing_role, connect=False, speak=False)
            await voice_channel.set_permissions(role, connect=True, speak=True)

            await message.channel.send(f'Role {role_name}, private text channel, and private voice channel created successfully!')
        except discord.Forbidden:
            await message.channel.send('Bot does not have permission to create roles or channels.')
        except discord.HTTPException as e:
            await message.channel.send(f'Error creating role or channel: {e}')



client.run(TOKEN) # type: ignore

import os
import random
import discord

 
GUILD = 'Collectif #Etsi'
CHANNEL_ID = "1192244304798818369"

intents = discord.Intents.default()
#intents.guilds = True
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

    if message.content.startswith('/role'):
        # Extracting the role name from the message
        _, role_name = message.content.split(" ", 1)

        # Finding the role in the guild
        role = discord.utils.get(message.guild.roles, name=role_name)

        if role:
            # Adding the role to the author of the message
            await message.author.add_roles(role)
            await message.channel.send(f'Role {role_name} added to {message.author.mention}')
        else:
            await message.channel.send(f'Role {role_name} not found in the server.')


    if message.content.startswith('/create_role'):
        # Extracting the role name from the message
        _, role_name = message.content.split(" ", 1)

        # Creating the role in the guild
        try:
            role_color = discord.Color(random.randint(0, 0xFFFFFF))  # Random color
            role = await message.guild.create_role(name=role_name, color=role_color)

            # Creating a category for the channels
            category = await message.guild.create_category(role_name)

            # Creating a private text channel with the same name as the role
            channel = await category.create_text_channel(role_name)

            # Setting channel permissions to only allow the role to access it
            await channel.set_permissions(role, read_messages=True, send_messages=True)

            await message.channel.send(f'Role {role_name} and private channel created successfully!')
        except discord.Forbidden:
            #await message.channel.send('Bot does not have permission to create roles or channels.')
            pass
        except discord.HTTPException as e:
            await message.channel.send(f'Error creating role or channel: {e}')


client.run(TOKEN) # type: ignore
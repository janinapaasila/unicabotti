import discord
from bs4 import BeautifulSoup
import requests

def parser(url, command) -> str:
    result = requests.get(url)
    parsed = BeautifulSoup(result.text, 'xml')
    tag = parsed.find_all('description')
    text = tag[1].string
    parts = text.split("<br>")

    response = f"`{command}`\n"
    for part in parts:
        subparts = part.split("*, ")
        part = ''.join(subparts)
        response += "\n" + part[:-1]
    response = response[:-2]

    return response

def vege(command) -> str:
    url_lista = ['https://www.unica.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1920&language=fi',
                 'https://www.unica.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1995&language=fi',
                 'https://www.unica.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1970&language=fi']

    response = f"`{command}`\n\n"

    for url in url_lista:
        result = requests.get(url)
        parsed = BeautifulSoup(result.text, 'xml')
        tag = parsed.find_all('description')
        text = tag[1].string
        parts = text.split("<br>")

        if url == url_lista[0]:
            response += f"`[assari]`\n"
        elif url == url_lista[1]:
            response += f"`[galilei]`\n"
        else:
            response += f"`[maccis]`\n"

        if url == url_lista[1]:
            response += parts[0]
        else:
            response += parts[0] + parts[1]
        subparts = response.split("*, ")
        response = ''.join(subparts)
    response = response[:-2]

    return response

def run_unicabotti():
    TOKEN = 'insert token here'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} on toiminnassa!")

    @client.event
    async def on_message(message):
        if message.author != client.user:
            command = str(message.content)
            if command == "!commands":
                await message.channel.send("Unica-botin komennot:\n\n"
                                           "`!assari` = Tulostaa Assarin päivän ruokalistan\n"
                                           "`!galilei` = Tulostaa Galilein päivän ruokalistan\n"
                                           "`!maccis` = Tulostaa Macciksen päivän ruokalistan\n"
                                           "`!vege` = Tulostaa kaikkien päivän kasvisruokalistat")
            elif command == "!assari":
                await message.channel.send(parser('https://www.unica.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1920&language=fi',command))
            elif command == "!galilei":
                await message.channel.send(parser('https://www.unica.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1995&language=fi',command))
            elif command == "!maccis":
                await message.channel.send(parser('https://www.unica.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1970&language=fi',command))
            elif command == "!vege":
                await message.channel.send(vege(command))
            elif command[0] == "!":
                await  message.channel.send(f"Komentoa `{command}` ei ole olemassa.")

    client.run(TOKEN)
from bs4 import BeautifulSoup
import requests

url_lista = ['https://www.unica.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1920&language=fi',
             'https://www.unica.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1995&language=fi',
             'https://www.unica.fi/modules/MenuRss/MenuRss/CurrentDay?costNumber=1970&language=fi']

response = f"`command`\n\n"

for url in url_lista:
    result = requests.get(url)
    parsed = BeautifulSoup(result.text, 'xml')
    tag = parsed.find_all('description')
    text = tag[1].string
    parts = text.split("<br>")

    if url == url_lista[0]:
        response += "`!vege -> assari`\n"
    elif url == url_lista[1]:
        response += "`!vege -> galilei`\n"
    else:
        response += "`!vege -> maccis`\n"

    if url == url_lista[1]:
        response += parts[0]
    else:
        response += parts[0] + parts[1]
    subparts = response.split("*, ")
    response = ''.join(subparts)

response = response[:-2]
print(response)
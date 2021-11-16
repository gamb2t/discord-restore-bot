import requests, config

URL = "https://discordapp.com/api/v9"

def add_role(guildid,userid,roleid):
        url = f"{URL}/guilds/{guildid}/members/{userid}/roles/{roleid}"

        botToken = config.token

        headers = {
            "Authorization" : f"Bot {botToken}",
            'Content-Type': 'application/json'
        }

        response = requests.put(url=url, headers=headers)
        print(response.json)

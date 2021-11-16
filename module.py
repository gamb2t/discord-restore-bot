import config, requests, asyncio, sqlite3

async def exchange_code(code):
    data = {
      'client_id': config.CLIENT_ID,
      'client_secret': config.CLIENT_SECRET,
      'grant_type': 'authorization_code',
      'code': code,
      'redirect_uri': config.REDIRECT_URI
    }
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    while True:
        r = requests.post('%s/oauth2/token' % config.API_ENDPOINT, data=data, headers=headers)
        if (r.status_code != 429):
            break

        limitinfo = r.json()
        await asyncio.sleep(limitinfo["retry_after"] + 2)
    return False if "error" in r.json() else r.json()

async def refresh_token(refresh_token):
    data = {
        'client_id': config.CLIENT_ID,
        'client_secret': config.CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    while True:
        r = requests.post('%s/oauth2/token' % config.API_ENDPOINT, data=data, headers=headers)
        if (r.status_code != 429):
            break

        limitinfo = r.json()
        await asyncio.sleep(limitinfo["retry_after"] + 2)

    print(r.json())
    return False if "error" in r.json() else r.json()

async def add_user(access_token, guild_id, user_id):
    while True:
        jsonData = {"access_token" : access_token}
        header = {"Authorization" : "Bot " + config.token}
        r = requests.put(f"{config.API_ENDPOINT}/guilds/{guild_id}/members/{user_id}", json=jsonData, headers=header)
        if (r.status_code != 429):
            break

        limitinfo = r.json()
        await asyncio.sleep(limitinfo["retry_after"] + 2)

    if (r.status_code == 201 or r.status_code == 204):
        return True
    else:
        print(r.json())
        return False

def opendb():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    return con,cur

async def get_user_profile(token):
    header = {"Authorization" : "Bearer " + token}
    res = requests.get("https://discordapp.com/api/v8/users/@me", headers=header)
    print(res.json())
    if (res.status_code != 200):
        return False
    else:
        return res.json()
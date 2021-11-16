import asyncio, role
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from requests.api import get
from module import exchange_code, opendb, get_user_profile

app = FastAPI()

@app.get("/callback")
async def callback(code : str):
    exchange_res = await exchange_code(code)
    if exchange_code == False:
        return "권한이 부여되지 않았습니다"
    profile = await get_user_profile(exchange_res["access_token"])
    if profile == False:
        return "권한이 부여되지 않았습니다"
    con,cur = opendb()
    cur.execute("INSERT INTO users VALUES (?, ?);", (profile["id"], exchange_res["refresh_token"]))
    con.commit()
    con.close()
    role.add_role("서버아이디",profile["id"],"인증 역할 아이디")
    return RedirectResponse("https://discord.com/oauth2/authorized")

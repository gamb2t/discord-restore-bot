import discord, sqlite3, config
from module import opendb, refresh_token, add_user

client = discord.Client()

@client.event
async def on_message(msg):
    if msg.guild == None:
        return

    if msg.author.id == msg.guild.owner_id:
        if msg.content == f"!복구 {config.recover_key}":
            await msg.channel.send("복구 중입니다...")
            con,cur = opendb()
            cur.execute("SELECT * FROM users;")
            users = cur.fetchall()
            
            for user in list(set(users)):
                try:
                    new_token = await refresh_token(user[1])
                    if new_token != False:
                        cur.execute("UPDATE users SET refresh_token = ? WHERE  id == ?;", (new_token["refresh_token"], user[0]))
                        con.commit()
                        await add_user(new_token["access_token"], msg.guild.id, user[0])
                except:
                    pass
            
            await msg.channel.send("복구 성공")

        if msg.content == "!안내":
            try:
                await msg.delete()
            except:
                pass
            await msg.channel.send(embed=discord.Embed(color=0x32cd32, title="인증 시스템", description=f"[인증하]({config.oauth2_url})를 클릭하시면\n인증 역할을 바로 받으실 수 있습니다."))

    

client.run(config.token)

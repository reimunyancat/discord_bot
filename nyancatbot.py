from pytube import YouTube
from nextcord import *
import asyncio
import os
import datetime
from dotenv import load_dotenv

try: os.mkdir("mp4")
except: ...
try: os.mkdir("mp3")
except: ...

load_dotenv()

TOKEN = os.getenv("TOKEN")
CLIENT = Client()

@CLIENT.event
async def on_ready():
    print(f"Bot is ready as {CLIENT.user}")

@CLIENT.slash_command(name="ping")
async def pingpong(inter: Interaction):

    ping = int(round(CLIENT.latency * 1000))
    text = f"🏓 pong {ping}ms"
    await inter.send(text)
    
@CLIENT.slash_command(name="youtube")
async def youtube(inter: Interaction):...
            

@youtube.subcommand(name="mp4", description="Extracts video from YouTube to mp4")
async def mp4(inter: Interaction , url: str):
    await inter.response.defer()
    
    yt = YouTube(url)
    title = yt.title

    timestamp = int(datetime.datetime.now().timestamp())
    async def down(url: str) -> str:
        file_name = await asyncio.to_thread(yt.streams.filter(only_audio=False).first().download, filename=f"mp4/{timestamp}.mp4")
        return file_name
    
    await inter.followup.send(title)
    file_name = await asyncio.create_task(down(url))
    await inter.followup.send(file=File(f"{file_name}"))
    os.remove(file_name)

@youtube.subcommand(name="mp3", description="Extracts audio from YouTube to mp3")
async def mp3(inter: Interaction , url: str):
    await inter.response.defer()

    yt = YouTube(url)
    title = yt.title

    timestamp = int(datetime.datetime.now().timestamp())
    async def down(url: str) -> str:
        file_name = await asyncio.to_thread(yt.streams.filter(only_audio=True).first().download, filename=f"mp3/{timestamp}.mp3")
        return file_name
    await inter.followup.send(title)
    file_name = await asyncio.create_task(down(url))
    await inter.followup.send(file=File(f"{file_name}"))
    os.remove(file_name)

    
@CLIENT.slash_command(name="en_to_wingding", description="Converts English text to Wingding text")
async def en_to_wingding(inter: Interaction, text: str):
    await inter.response.defer()

    wingding_map = {
    'A': '✌︎', 'B': '👌︎', 'C': '👍︎', 'D': '👎︎', 'E': '☜︎', 'F': '☞︎', 'G': '☝︎', 'H': '☟︎', 'I': '✋︎', 'J': '☺︎', 'K': '😐︎', 'L': '☹︎', 'M': '💣︎', 'N': '☠︎', 'O': '⚐︎', 'P': '🏱︎', 'Q': '✈︎', 'R': '☼︎', 'S': '💧︎', 'T': '❄︎', 'U': '🕆︎', 'V': '✞︎', 'W': '🕈︎', 'X': '✠︎', 'Y': '✡︎', 'Z': '☪︎',
    'a': '♋︎', 'b': '♌︎', 'c': '♍︎', 'd': '♎︎', 'e': '♏︎', 'f': '♐︎', 'g': '♑︎', 'h': '♒︎', 'i': '♓︎', 'j': '♑︎', 'k': '🙵', 'l': '●︎', 'm': '❍︎', 'n': '■︎', 'o': '□︎', 'p': '◻︎', 'q': '❑︎', 'r': '❒︎', 's': '⬧︎', 't': '⧫︎', 'u': '◆︎', 'v': '❖︎', 'w': '⬥︎', 'x': '⌧︎', 'y': '⍓︎', 'z': '⌘︎',
    '`': '♊︎', '1': '📂︎', '2': '📄︎', '3': '🗏︎', '4': '🗐︎', '5': '🗄︎', '6': '⌛︎', '7': '🖮︎', '8': '🖰︎', '9': '🖲︎', '0': '📁︎', '-': '📫︎', '=': '🖬︎', '\\': 'ॐ︎', '[': '☯︎', ']': '☸︎', ';': '🖴︎', "'": '🕯︎', ',': '📪︎', '.': '📬︎', '/': '📭︎', '~': '❞︎', '!': '✏︎', '@': '@', '#': '✁︎', '$': '👓︎', '%': '🕭︎', '^': '♈︎', '&': '🕮︎', '*': '🖂︎', '(': '🕿︎', ')': '✆︎', '_': '♉︎', '+': '🖃︎', '|': '✿︎', '{': '❀︎', '}': '❝︎', ':': '🖳︎', '"': '✂︎', '<': '🖫︎', '>': '✇︎', '?': '✍︎'
    }

    # 윙딩어로 변환
    output = ""
    for char in text:
        if char in wingding_map:
            output += wingding_map[char]
        else:
            output += char

    await inter.followup.send(f"입력 : {text}")
    # 변환된 윙딩어 텍스트 출력
    await inter.followup.send(f"출력 : {output}")

if __name__ == "__main__":
    CLIENT.run(TOKEN)

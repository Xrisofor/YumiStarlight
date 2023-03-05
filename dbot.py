#Discord Lib
import discord
from discord.ext import commands

#OpenAI
import openai

#Lang
from lang import languages; from lang import script_type
from lang import script_gen

#YouTube
from youtube_dl import YoutubeDL

#Dev
#from background import keep_alive

default_language = "en"
config = {
  'token': 'MTA3MjQzNTg1MzY5NzIyODg2Mw.GIgxxr.Ozx77hWtZPiP196XFJEaWtWmMaY0tRRCR1xJC0',
  'prefix': '$',
}

openai.api_key = "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"
bot = commands.Bot(command_prefix=config['prefix'])

def getText(key, lang=default_language):
    return languages[lang][key]

@bot.event
async def on_ready():
  print(f'{bot.user.name} has connected to Discord!')
  await bot.change_presence(status=discord.Status.online,
                            activity=discord.Game("Water, money, artificial intelligence"))

@bot.command()
async def helpme(ctx):
    await ctx.reply(getText("help_msg", default_language))


@bot.command()
async def language(ctx, lang):
    global default_language
    lang = lang.lower()
    if lang in languages.keys():
        default_language = lang
        await ctx.reply(getText("lang_update", lang))
    else:
        await ctx.reply(getText("unsupported_lang", lang))

@bot.command()
async def chat(ctx, *arg):
    prompt = ' '.join(arg)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    sc_type = ""
    for sc_tp in script_type:
        if sc_tp in prompt.lower():
            sc_type = script_type[sc_tp]

    for sc_gn in script_gen:
        if sc_gn in prompt.lower():
            response = f"```{sc_type}\n" + response + "```"

    await ctx.reply(response)


@bot.command()
async def nick(ctx):
  global default_language
  prompt = getText("nick_prompt", default_language)
  response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
  ).choices[0].text.strip()
  author = ctx.author
  try:
    await author.edit(nick=response)
    await ctx.reply(getText("new_nick", default_language) + response + "!")
  except Exception as e:
    await ctx.reply(getText("error", default_language) + e)


#YouTube
YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

@bot.command()
async def play(ctx, url):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice == None:
      vc = await ctx.message.author.voice.channel.connect()
    else:
       vc = await ctx.message.author.voice.channel

    with YoutubeDL(YDL_OPTIONS) as ydl:
      if 'https://' in url:
        info = ydl.extract_info(url, download=False)
      else:
        info = ydl.extract_info(f'ytsearch:{url}', download=False)['entries'][0]

    link = info['formats'][0]['url']

    vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\arabo\\Documents\\Python\\discord bt\\ffmpeg\\ffmpeg.exe", source=link, **FFMPEG_OPTIONS))

    video_tl = info.get('title', None)
    emb = discord.Embed(title='Music', colour=discord.Color.green(), description=f'Played: {video_tl}')
    await ctx.send(embed=emb)

#keep_alive()
bot.run(config['token'])
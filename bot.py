import os
import Queue
import asyncio
import discord, query, dropdown
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio

# Token: NjAxNzg0ODk1MTg2MTQxMjI1.G7VehJ.bBehsIiwtChpLawSOHwbJ5_xbEItLE3NNkb9To
#Chisa, please
bot = commands.Bot(command_prefix=commands.when_mentioned_or("Chisa, please "), intents=discord.Intents.all())
queue = Queue.MyQueue()

def check_queue(ctx, name):
    voice = ctx.guild.voice_client
    queue.get_next_track()


class MyCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=5.0)
    async def printer(self):
        print(self.index)
        self.index += 1


@bot.event
async def on_ready():
    print("Hello, Chisa is ready to work!")

async def on_command_error(ctx, error):
    await ctx.send("error")




@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"I say Pong! {round(bot.latency * 1000)}")


@bot.command(name="greet")
async def greet(ctx):
    # em = discord.Embed(title= "Chisa", description=" ", color=0x41BFBF)
    #
    # em.add_field(name="Online Test", value="Chisa is ready!")
    msg = await ctx.send("Hello, my name is Chisa, I am a bot that is connected to Stalight_'s harddrive that plays songs!")
    # await ctx.send(embed=em)


@bot.command(name="echo")
async def echo(ctx, *, message: str):

    await ctx.send(message)


@bot.command(pass_context=True, name="find")
async def find(ctx, *, message):
    if ctx.voice_client:
        msg = await ctx.send("Searching!")
        path_source = query.find_music(message)
        if path_source == []:
            await ctx.send("I cannot find such song!")
        else:

            if len(path_source) < 10:
                options = path_source[:len(path_source)]
            else:
                options = path_source[:10]

            new_view = dropdown.MyView(options, ctx)
            em = discord.Embed(title="Chisa", description="Here are the songs: \n" + new_view.list_songs, color=0xfcc9b9)
            emb = await ctx.send(embed=em)

            v = await ctx.send(view=new_view)

            await asyncio.sleep(5)
            await ctx.message.delete()
            await emb.delete()
            await v.delete()
            await msg.delete()

    else:
        if await ctx.invoke(bot.get_command('join')):
            await ctx.invoke(bot.get_command('find'), message=message)


@find.error
async def find(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing the song name!")


@bot.command(pass_context=True, name="pause")
async def pause(ctx):
    if ctx.voice_client:
        ctx.voice_client.pause()
        await ctx.send("Pausing!")
    else:
        await ctx.send("Please enter a voice channel!")
        return False

@bot.command(pass_context=True, name="skip")
async def skip(ctx):
    if ctx.voice_client:
        voice = ctx.guild.voice_client
        voice.pause()
        source = queue.get_next_track()
        voice.play(source, after=lambda x: check_queue(ctx))
        await ctx.send("Skipped!")
    else:
        await ctx.send("Please enter a voice channel!")
        return False

@bot.command(pass_context=True, name="resume")
async def resume(ctx):
    if ctx.voice_client:
        ctx.voice_client.resume()
        await ctx.send("Resuming!")
    else:
        await ctx.send("Please enter a voice channel!")
        return False


@bot.command(pass_context=True, name="join")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        return True

    else:
        await ctx.send("Please enter a voice channel!")
        return False


@bot.command(pass_context=True, name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.pause()
        await ctx.guild.voice_client.disconnect()
        queue.purge()
    else:
        await ctx.send("I'm not in a voice channel!")


@bot.command(name="repeat_queue")
async def repeat_queue(ctx):
    result = queue.change_repeatable()
    if result:
        await ctx.send("repeat is on!")
    else:
        await ctx.send("repeat is off!")

@bot.command(name="list_queue")
async def list_queue(ctx):
    await ctx.send(queue.list_queue())


def run_bot():

    bot.run("NjAxNzg0ODk1MTg2MTQxMjI1.G7VehJ.bBehsIiwtChpLawSOHwbJ5_xbEItLE3NNkb9To")

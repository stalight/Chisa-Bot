import discord.ui
from discord import FFmpegPCMAudio

import bot

def check_queue(ctx):
    if not bot.queue.is_empty():
        voice = ctx.guild.voice_client
        source = bot.queue.get_next_track()
        voice.play(source, after=lambda x: check_queue(ctx))




class SongDropdown(discord.ui.Select):
    def __init__(self, options, ctx):
        # options=[
        #     discord.SelectOption(label="A", description="SSS"),
        #     discord.SelectOption(label="AA", description="SSS"),
        #     discord.SelectOption(label="AAA", description="SSS")
        # ]
        # self.c = ctx
        # self.options = option
        self.paths = dict()
        self.ctx = ctx
        selects = []
        songs = []
        for i in range(len(options)):
            song = options[i][1]
            path = options[i][0] + "/" + song
            self.paths[song] = path
            item_label = f"{i + 1} : " + song
            songs.append(item_label)
            select_option = discord.SelectOption(label=item_label, description=song)
            selects.append(select_option)

        self.list_songs = '\n'.join(songs)

        super().__init__(placeholder="Here are the related Songs!", options=selects, min_values=1, max_values=1)

    async def callback(self,
                       interaction: discord.Interaction):  # the function called when the user is done selecting options
        song_name = self.values[0][4:]
        await interaction.response.send_message(f"{song_name} has been added!", delete_after=10)
        path = self.paths[song_name]
        source = FFmpegPCMAudio(executable='C:/Users/User/FFMPEG/ffmpeg.exe',
                                source=path)
        bot.queue.add(song_name, source)

        voice = self.ctx.guild.voice_client
        if not self.ctx.guild.voice_client.is_playing() and bot.queue.get_position() == 0:
            bot.queue.increase_position()
            player = voice.play(source, after=lambda x: check_queue(self.ctx))

        # source = FFmpegPCMAudio(executable='C:/Users/User/FFMPEG/ffmpeg.exe',
        #                         source=path)
        # player = self.ctx.voice_client.play(source)-tes


class MyView(discord.ui.View):
    def __init__(self, options, ctx):
        dropdown = SongDropdown(options, ctx)
        self.list_songs = dropdown.list_songs

        super().__init__()
        self.add_item(dropdown)

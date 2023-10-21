import discord
from ast import alias
from discord.ext import commands
from yt_dlp import YoutubeDL


class music_cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = None
    
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download = False)['entries'][0]
            except Exception:
                return False
        return {'source': info['url'], 'title': info['title']}
    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            music_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(music_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            music_url = self.music_queue[0][0]['source']
            if self.vc == None or not self.vc.is_connected():
                self.vc == await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(music_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p", "playing"], help="I think it's pretty obvious. You're such a player.")
    async def play(self, ctx, *args):
        query = " ".join(args)
        vc_channel = ctx.author.voice.channel

        if vc_channel is None:
            await ctx.send("Connect to VC.")
        elif self.is_paused:
            self.vc.resume
        else:
            video = self.search_yt(query)
            if type(video) == type(True):
                await ctx.send("Incorrect format, dumbass.")
            else:
                await ctx.send("Added to queue.")
                self.music_queue.append([video, vc_channel])
                if not self.is_playing:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="What do you think a command called __pause__ does?")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="resume", aliases=["r"], help="Care to explain the gap in your resume?")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Jojo part 1 and 2.")
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q"], help="The word queue is just Q followed by 4 silent letters.")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            if i > 6: break
            retval += self.music_queue[i][0]['title'] + '\n'
        
        if retval != "":
            await ctx.send(retval)

        else:
            await ctx.send("Empty queue.")

    @commands.command(name="clear", aliases=["c", "bin"], help="Let me be clear.")
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Domain expanded, no more music.")

    @commands.command(name="leave", aliases=["disconnect", "d", "l"], help="Get that ass banned.")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()

async def setup(bot):
    await bot.add_cog(music_cog(bot)) 
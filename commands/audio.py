from discord.ext import commands
import discord


from youtubesearchpython import VideosSearch
import yt_dlp


class Music(commands.Cog):
    """\"Voice\" commands"""

    def __init__(self, bot):
        self.bot: discord.Bot = bot

    @commands.command()
    async def join(self, ctx: commands.Context):
        """Join your voice channel"""
        channel = ctx.author.voice.channel
        if channel:
            await channel.connect()
        else:
            await ctx.send("You're not in a voice channel!")

    @commands.command()
    async def leave(self, ctx: commands.Context):
        """Leave your voice channel"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("I'm not in a voice channel!")

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="CKY2K | !help"))

    @commands.command()
    async def play_raw(self, ctx, *, url_to_audio: str):
        """Plays an audio file or stream from a URL."""
        voice_client = ctx.voice_client

        if not voice_client:
            await ctx.reply("I'm not connected to a voice channel!")
            return

        if not url_to_audio.startswith(('http://', 'https://')):
            await ctx.reply("Please provide a valid file path or URL!")
            return

        if voice_client.is_playing():
            voice_client.stop()

        audio_source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(url_to_audio))
        voice_client.play(audio_source, after=lambda e: print(
            f"Player error: {e}") if e else None)

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=url_to_audio.split("/")[-1].split("?")[0]))

        await ctx.reply(f"Now playing: {url_to_audio}")

    @commands.command()
    async def stop(self, ctx: commands.Context):
        """Stop the audio source"""
        voice_client = ctx.voice_client

        if not voice_client:
            await ctx.reply("I'm not connected to a voice channel!")
            return
        if voice_client.is_playing():
            voice_client.stop()
        else:
            await ctx.reply("I'm not playing anything!")

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="CKY2K | !help"))

    @commands.command()
    async def yts(self, ctx: commands.Context, *, search_query: str):
        """Search YouTube"""
        search = VideosSearch(search_query, limit=10)
        results = search.result()
        embed = discord.Embed(
            title=f"Results for '**{search_query}**'",
            color=0xff0000
        )
        for result in results['result']:
            embed.add_field(
                name=f"{result['title']}",
                value=f"<https://www.youtube.com/watch?v={result['id']}>",
                inline=False
            )
        await ctx.reply(embed=embed)

    @commands.command()
    async def ytp(self, ctx: commands.Context, *, url: str):
        """Play audio from YouTube"""
        voice_client = ctx.voice_client

        if not voice_client:
            await ctx.reply("I'm not connected to a voice channel!")
            return

        # if not url.startswith(('http://', 'https://')):
        #     await ctx.reply("Please provide a valid YouTube URL!")
        #     return

        if voice_client.is_playing():
            voice_client.stop()

        ydl_opts = {'format': 'bestaudio'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            audio_url = info_dict['url']

        audio_source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(audio_url))
        voice_client.play(audio_source, after=lambda e: print(
            f"Player error: {e}") if e else None)

        await ctx.reply(f"Now playing: *{info_dict['title']}*")

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=info_dict['title']))

    @commands.command()
    async def volume(self, ctx: commands.Context, volume: int):
        """Change the player's volume"""

        if volume < 0 or volume > 100:
            await ctx.reply("Please enter a value between 0 and 100!")
            return

        voice_client = ctx.voice_client

        if not voice_client:
            await ctx.reply("I'm not in a voice channel!")
            return

        voice_client.source.volume = volume / 100
        await ctx.reply(f"Changed volume to {volume}%")
    
    @ytp.before_invoke
    @play_raw.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


async def setup(bot):
    await bot.add_cog(Music(bot))

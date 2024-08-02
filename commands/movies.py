from discord.ext import commands
import discord
from utils.utils import search_movie, search_movie_id, get_movie_poster, get_movie_banner
import random
from time import sleep


class Movies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.movies = []

    @commands.command()
    @commands.has_any_role("Admin", "Owner", "Moderator")
    async def list_movies(self, ctx):
        """List requested movies(mods+ only)"""
        embed = discord.Embed(
            title=f"Requested movies",
            color=0xff0000
        )
        for movie_id in self.movies:
            movie = search_movie_id(movie_id)
            embed.add_field(
                name=movie.get('title', 'Unknown Title'),
                value=movie.get('overview', 'No description available'),
                inline=False
            )
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_any_role("Admin", "Owner", "Moderator")
    async def random_movie(self, ctx):
        """Select a random movie from requests(mod+ only)"""
        if len(self.movies) <= 0:
            await ctx.reply("There are no movies to choose from")
            return
        elif len(self.movies) == 1:
            await ctx.reply(f"There is only one movie, so I guess I'll pick...")
        else:
            await ctx.reply(f"Out of {len(self.movies)} movies, I choose..")
        chosen_movie = random.choice(self.movies)
        movie = search_movie_id(chosen_movie)
        embed = discord.Embed(
            title=movie.get('title', 'Unknown Title'),
            description=movie.get("overview", "No description available"),
            color=0xff0000
        )
        poster = get_movie_poster(chosen_movie)
        banner = get_movie_banner(chosen_movie)

        embed.set_image(url=banner)
        embed.set_thumbnail(url=poster)

        sleep(2)
        await ctx.send(embed=embed)
        # await ctx.send(embed=embed)

    @commands.command()
    async def request(self, ctx, *args):
        """Request a movie to be played"""
        movie_name = ' '.join(args).strip()

        # Check if the input is numeric
        if movie_name.isdigit():
            # Treat the input as a movie ID
            movie_id = int(movie_name)
            result = search_movie_id(movie_id)

            if result.get('title'):
                title = result['title']
                if movie_id in self.movies:
                    await ctx.reply(f"`{title}` has already been requested!")
                    return

                else:
                    self.movies.append(movie_id)
                await ctx.reply(f"Request for `{title}` sent successfully")
            else:
                await ctx.reply(f"No movie found with ID '**{movie_id}**'.")
            return

        # If the input is not numeric, perform a search
        results = search_movie(movie_name)

        if results['count'] == 0:
            await ctx.reply(f"No results found for '**{movie_name}**'.")
        elif results['count'] == 1:
            # Directly fetch the movie details
            movie_id = results["results"][0]["id"]
            result = search_movie_id(movie_id)
            title = result.get('title')
            if movie_id in self.movies:
                await ctx.reply(f"`{title}` has already been requested!")
                return

            else:
                self.movies.append(movie_id)

            await ctx.reply(f"Request for `{title}` sent successfully")
        else:
            await ctx.reply(f"Multiple results found for '**{movie_name}**'.\n"
                            f"Please use `!search` to see all options and get the exact ID.")

    @commands.command()
    async def search(self, ctx, *args):
        """Search for movies"""
        movie_name = ' '.join(args)
        print(f"searching for movie '{movie_name}'")
        limit = 10
        results = search_movie(movie_name, limit)
        print(results)
        embed = discord.Embed(
            title=f"Results for '**{movie_name}**'",
            color=0xff0000
        )
        for result in results["results"]:
            embed.add_field(
                name=f"{result["title"]} || *{result["id"]}*",
                value=result["overview"],
                inline=False
            )
        additional_count = results['count'] - limit
        footer_text = f"+{additional_count} more results" if additional_count > 0 else "No more results"
        embed.set_footer(text=footer_text)
        # embed.add_field(name="test", value="test", inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def movie_info(self, ctx, *args):
        """Get information about a movie"""
        movie_name = ' '.join(args).strip()
        info_embed = discord.Embed()
        if movie_name.isdigit():
            movie_id = int(movie_name)
            result = search_movie_id(movie_id)

            info_embed.title = result.get("title", "No title found")
            info_embed.description = result.get("overview", "No description found")
            info_embed.description += f"\n\n**Budget:** ${int(result.get('budget')):,}" \
                if int(result.get('budget')) > 0 \
                else f"\n\n**Budget:** *Unknown*"
            poster = get_movie_poster(movie_id)
            banner = get_movie_banner(movie_id)

            info_embed.set_image(url=banner)
            info_embed.set_thumbnail(url=poster)

            await ctx.reply(embed=info_embed)
            # await ctx.reply(result) # debug thing
            return

        results = search_movie(movie_name)

        if results['count'] == 0:
            await ctx.reply(f"No results found for '**{movie_name}**'.")
        elif results['count'] == 1:
            movie_id = results["results"][0]["id"]
            result = search_movie_id(movie_id)

            info_embed.title = result.get("title", "No title found")
            info_embed.description = result.get("overview", "No description found")
            info_embed.description += f"\n\n**Budget:** ${int(result.get('budget')):,}"\
                if int(result.get('budget')) > 0\
                else f"\n\n**Budget:** *Unknown*"

            poster = get_movie_poster(movie_id)
            banner = get_movie_banner(movie_id)

            info_embed.set_image(url=banner)
            info_embed.set_thumbnail(url=poster)

            await ctx.reply(embed=info_embed)
            # await ctx.reply(result)  # debug thing
            return
        else:
            await ctx.reply(f"Multiple results found for '**{movie_name}**'.\n"
                            f"Please use `!search` to see all options and get the exact ID.")


async def setup(bot):
    await bot.add_cog(Movies(bot))

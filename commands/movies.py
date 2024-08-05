from discord.ext import commands
import discord
from utils.utils import search_movie, search_movie_id, get_movie_poster, get_movie_banner
from utils.config import get_webui_key
import random
from time import sleep
import requests
from typing import Optional, Union


class Movies(commands.Cog):
    """Commands for requesting and viewing movies"""
    def __init__(self, bot):
        self.bot = bot
        # self.movies = []
        self.webui_key = get_webui_key()

    @commands.command()
    @commands.has_any_role("Admin", "Owner", "Moderator")
    @commands.guild_only()
    async def list_movies(self, ctx):  # list the currently requested movies. in self.movies
        """List requested movies(mods+ only)"""
        embed = discord.Embed(  # create an embed for the movies
            title=f"Requested movies",
            color=0xff0000
        )
        try:
            resp = requests.get("http://localhost:3000/get-movies")
            json_data = resp.json()
            if json_data["count"] == 0:
                await ctx.reply("No movies have been requested")
                return
            for movie in json_data["movies"]:
                embed.add_field(name=movie["title"], value=movie["desc"], inline=False)
        except requests.exceptions.RequestException as e:
            await ctx.reply(f"An error occurred getting movies: {e}")
            return
        await ctx.reply(embed=embed)  # reply with that embed

    @commands.command()
    @commands.has_any_role("Admin", "Owner", "Moderator")
    @commands.guild_only()
    async def random_movie(self, ctx):  # select a random movie from self.movies
        """Select a random movie from requests(mod+ only)"""
        movies_resp = requests.get("http://localhost:3000/get-movies")
        movies = movies_resp.json()
        if movies["count"] <= 0:  # if there are no requested movies
            await ctx.reply("There are no movies to choose from")
            return
        elif movies["count"] == 1:  # if there is only one
            await ctx.reply(f"There is only one movie, so I guess I'll pick...")
        else:  # anything else
            await ctx.reply(f"Out of {movies["count"]} movies, I choose..")
        chosen_movie = random.choice(movies["movies"])
        movie = random.choice(movies["movies"])
        embed = discord.Embed(
            title=movie["title"],
            description=movie["desc"],
            color=0xff0000
        )
        poster = get_movie_poster(chosen_movie["id"])  # get the movies poster
        banner = get_movie_banner(chosen_movie["id"])  # get the movies banner

        embed.set_image(url=banner)  # set the image to the movies banner
        embed.set_thumbnail(url=poster)  # set the thumbnail to the movie poster

        sleep(2)  # sleep for 2 seconds before sending it
        await ctx.send(embed=embed)  # send that embed
        # await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def request(self, ctx, *, movie_name: Optional[Union[str, int]]):  # request a movie, with id or name
        """Request a movie to be played"""
        # movie_name = ' '.join(args).strip() if args else ""
        if movie_name is None:
            await ctx.reply("A movie name or id is required!")
            return

        # Check if the input is numeric
        if movie_name.isdigit():  # if it is a number(as in a movies id)
            # Treat the input as a movie ID
            movie_id = int(movie_name)
            result = search_movie_id(movie_id)  # search by id only

            if result.get('title'):
                title = result['title']
                desc = result.get("overview", "No description")
                existing_movies_resp = requests.get("http://localhost:3000/get-movies")
                existing_movies_json = existing_movies_resp.json()
                existing_movie_ids = [m["id"] for m in existing_movies_json["movies"]]
                if str(movie_id) in existing_movie_ids:
                    await ctx.reply(f"`{title}` has already been requested!")
                    return
                else:
                    data = {
                        "title": title,
                        "desc": desc,
                        "id": movie_id
                    }
                    headers = {'Authorization': self.webui_key}
                    api_resp = requests.post("http://localhost:3000/add-movie", data=data, headers=headers)
                if api_resp.status_code == 200:
                    response_json = api_resp.json()
                    if response_json.get("status") == "success":
                        await ctx.reply(f"Request for `{title}` sent successfully")
                    else:
                        await ctx.reply("Movie was requested, but not updated in the web UI :(")
                else:
                    await ctx.reply("Failed to send request to the web UI :(")
            else:
                await ctx.reply(f"No movie found with ID '**{movie_id}**'.")
            return

        # If the input is not numeric, perform a search
        results = search_movie(movie_name)

        if results['count'] == 0:  # if there are no movies with that title
            await ctx.reply(f"No results found for '**{movie_name}**'.")
        elif results['count'] == 1:
            # Directly fetch the movie details
            movie_id = results["results"][0]["id"]
            result = search_movie_id(movie_id)
            title = result.get('title')
            desc = result.get('overview')
            existing_movies_resp = requests.get("http://localhost:3000/get-movies")
            existing_movies_json = existing_movies_resp.json()
            existing_movie_ids = [m["id"] for m in existing_movies_json["movies"]]
            if str(movie_id) in existing_movie_ids:
                await ctx.reply(f"`{title}` has already been requested!")
                return
            else:
                data = {
                    "title": title,
                    "desc": desc,
                    "id": movie_id
                }
                headers = {'Authorization': self.webui_key}
                api_resp = requests.post("http://localhost:3000/add-movie", data=data, headers=headers)
            if api_resp.status_code == 200:
                response_json = api_resp.json()
                if response_json.get("status") == "success":
                    await ctx.reply(f"Request for `{title}` sent successfully")
                else:
                    await ctx.reply("Movie was requested, but not updated in the web UI :(")
            else:
                await ctx.reply("Failed to send request to the web UI")
        else:
            await ctx.reply(f"Multiple results found for '**{movie_name}**'.\n"
                            f"Please use `!search` to see all options and get the exact ID.")

    @commands.command()
    @commands.guild_only()
    async def search(self, ctx, *, movie_name: Optional[str]):  # search for movies by name
        """Search for movies"""
        # movie_name = ' '.join(args)
        if movie_name is None:
            await ctx.reply("A movie name is required!")
        limit = 10
        results = search_movie(movie_name, limit)
        embed = discord.Embed(
            title=f"Results for '**{movie_name}**'",
            color=0xff0000
        )
        if results["count"] == 0:
            await ctx.reply(f"`{movie_name}` returned no results.")
        for result in results["results"]:  # for the movies add a field for each one foind in the search
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
    @commands.guild_only()
    async def movie_info(self, ctx, *args):  # get info about a specific movie
        """Get information about a movie"""
        movie_name = ' '.join(args).strip()
        info_embed = discord.Embed()
        if movie_name.isdigit():  # if it is an id(numeric)
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
            info_embed.description += f"\n\n**Budget:** ${int(result.get('budget')):,}" \
                if int(result.get('budget')) > 0 \
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

    @commands.command()
    @commands.has_any_role("Admin", "Owner", "Moderator")
    @commands.guild_only()
    async def reset_requests(self, ctx):
        """Reset requests"""
        headers = {'Authorization': self.webui_key}
        resp = requests.get("http://localhost:3000/reset-requests", headers=headers)
        if resp.status_code == 200 and resp.json().get("status") == "success":
            await ctx.reply("Requests reset")
        else:
            await ctx.reply("Failed to send requests: " + resp.text)


async def setup(bot):
    await bot.add_cog(Movies(bot))

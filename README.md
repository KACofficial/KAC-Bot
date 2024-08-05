# KAC-Bot

This is a discord bot's backend.  
The bot is for requesting movies, and having some fun.  
When the bot is ran it starts a web ui at `localhost:3000`.  
The webui is to show all of the requested movies.

## Setup
This setup guide is for LINUX ONLY.  
I haven't used windows in years.  

### you will need to clone this repo.  
- `git clone https://github.com/KACofficial/KAC-Bot.git`
- `cd KAC-Bot`

### Then setup a virtual enviroment(Optional but Recommended).
- `python3 -m venv .venv`
- `source .venv/bin/activate`

### Then install the requirements.
- `pip install -r requirements.txt`

### Then setup a `config.json` file like so.
```json
{
  "bot_token": "<YOUR_DISCORD_BOTS_TOKEN>",
  "tmdb_key": "<YOUR_TMDB_API_KEY>",
  "webui_key": "<A_KEY_FOR_THE_WEBUI>"
}
```
- `webui_key` is a custom secret key to be able to remove and manipulate movies, keep it secure,  
  - I recommend you generate one here: [lastpass.com/features/password-generator](https://www.lastpass.com/features/password-generator)

### Then you should be good to run it.
- `python3 main.py`

# Discord-Bot
This is a Discord bot written in Python using [discord.py](https://github.com/Rapptz/discord.py) that features various commands listed [here](#bot-commands). The commands are written as cogs found in the *modules* folder and can be easily implemented into an existing bot.

### Dependencies
* Python 3.6+
* [discord.py](https://github.com/Rapptz/discord.py)
* [requests](https://github.com/psf/requests)
* [wikipedia](https://github.com/goldsmith/Wikipedia)
* [translate](https://github.com/terryyin/translate-python)
* [python-dotenv](https://github.com/theskumar/python-dotenv)

## Installation
Download or clone the respository
```
git clone https://github.com/gkvong/Discord-Bot
```

To install any required dependencies:
```bash
pip install -r requirements.txt
```

## Setup
### Inviting the bot to your server
1. Create an account for the [Discord developer portal](https://discord.com/developers/applications).
2. Create a new application.
3. Navigate to **Bot** on the left sidebar and add a bot.
4. Navigate to the **OAuth2** tab on the left sidebar and select the `bot` box in the **SCOPES** section.
5. In the **BOT PERMISSIONS** section select the permissions you want the bot to have. Recommended minimum permissions are all the boxes under **TEXT PERMISSIONS** and `View Channels`.

### Obtaining your Discord token
1. In the [Discord developer portal](https://discord.com/developers/applications) navigate to **Bot**.
2. Copy the token and replace `[PASTE YOUR DISCORD BOT TOKEN HERE]` in *.env* with the token.

### Obtaining your OpenWeatherMap API ID
1. Create an account and sign in at [openweathermap.org](https://home.openweathermap.org).
2. On the top navigation bar, click on your username and go to [My API keys](https://home.openweathermap.org/api_keys).
3. Copy the key and replace `[PASTE YOUR OPENWEATHERMAP API ID HERE]` in *.env* with the token.

### Running the bot
To run the bot, execute *main.py*:
```
python main.py
```

## Bot Commands
Command       | Description
------------- | -------------
$help | Provides a brief description of the bot commands.
$ping | Get the latency of the bot.
$minesweeper | Play a game of minesweeper.
$trivia | Start a game of trivia.
$define \<query\> | Search for a definition from Google Dictionary.
$wiki \<query\> | Get the first few sentences of a Wikipedia page.
$translate \<to\> \<from\> \<text\> | Translate a message.
$weather \<city\> | Get the current weather in a city.
$forecast | Get the 7-day Sydney weather forecast.

## License
[MIT License](LICENSE)

## Acknowledgements
Thanks to [DeCoded-Void](https://github.com/DeCoded-Void) for [Minesweeper_discord.py](https://github.com/DeCoded-Void/Minesweeper_discord.py) where a large portion of the code in the minesweeper module was taken from.

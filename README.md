# 🤖 AI-Discord-Mod 🤖

AI-Discord-Mod is a Discord bot that utilizes OpenAI's GPT-3.5 API for text moderation and HuggingFaces' transformer model for image moderation. This bot helps maintain a safe and respectful environment in your Discord server.


## 🌟 Features

- Text moderation using OpenAI's GPT-3.5 API
- Image moderation using HuggingFaces' transformer model
- Warns and mutes users for inappropriate messages
- Configurable warning limit and mute duration


## 🚀 Getting Started

Follow these steps to set up your own instance of AI-Discord-Mod:


### 📋 Prerequisites

Ensure you have the following installed:
- Python 3.6 or later
- pip (Python package installer)

Install the necessary Python packages with the following commands:

```sh
pip install -r requirements.txt
pip install transformers datasets
pip install torch # or pip install tensorflow depending on your preference
```


## 🤖 Setting up a Discord Bot
  1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
  2. Click on "New Application". Give it a name and click on "Create".
  3. Go to the "Bot" tab and click on "Add Bot". You will see a message saying "A wild bot has appeared!", click "Yes, do it!".
  4. Under the "Token" section, click on "Copy". This will be your DISCORD_BOT_TOKEN. **Remember to keep this secret!**
  5. Go to the "OAuth2" tab, under "Scopes" tick "bot", then under "Bot Permissions" tick "Administrator".
  6. You will see a generated URL, use this URL to invite your bot to your Discord server.
## 🛠 Setting up the AI-Discord-Mod Project
  1. Clone this repository to your local machine:
     `git clone https://github.com/gravelBridge/AI-Discord-Mod.git`
  2. Navigate to the project directory:
     `cd AI-Discord-Mod`
  3. Copy the .env.template file and rename it to .env:
     `cp .env.template .env`
  4. Open the .env file in a text editor and replace the placeholders with your `OPENAI_API_KEY` and `DISCORD_BOT_TOKEN`. Set the `WARNINGS` and `MUTE_TIME` values as per your preference.
  5. Your .env file should look like this:
     ```
     # OPENAI_API_KEY: Your OpenAI API Key, must be connected to an account with a payment method.
     OPENAI_API_KEY=your_openai_api_key
     #DISCORD_BOT_TOKEN: Your Discord Bot Token that's in your Discord Server.
     DISCORD_BOT_TOKEN=your_discord_bot_token

     # WARNINGS: The number of warnings the bot should give before muting the user.
     WARNINGS=number_of_warnings
     # MUTE_TIME: How long the bot should mute the user for after all warnings are used up. Ex: 1s for 1 second, 3m for 3 minutes, 4h for four hours, 5d for five days.
     MUTE_TIME=duration_of_mute
     ```
  6. Save and close the `.env` file.


## 🏃 Running the Bot
To run the bot, navigate to the project directory and run:
`python ai-discord-moderator/discord_bot.py`

The bot should now be active in your Discord server and automatically moderate text and images based on the rules defined in the ai_discord_functions.py and discord_bot.py scripts.


## ⚠️ Note
This bot uses AI models which, while powerful, might not always make perfect decisions. It is recommended to have human moderators oversee the bot's actions for best results.


## 📝 License
This project is licensed under the GPL-3.0 License. See the LICENSE file for details.

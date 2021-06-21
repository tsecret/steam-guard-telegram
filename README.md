# History

As an owner of multiple steam accounts ~~and a lazy person~~, I got tired of using a phone to get a Steam Guard code every time I log into the account. (plus some accounts are not linked to my phone). So I build a simple telegram bot to manage my steam guard codes and would like to share with others who are having same issues with me  

# Installation and configuration

1. Install the required packages
```pip install -r requirements.txt```
2. Navigate to main directory, there you should find **accounts-sample.json** and **config-sample.py**
3. Rename **accounts-sample.json** to **accounts.json**, here is where you store the accounts.
4. Rename **config-sample.py** to **config.py** and open it. 
    - TELEGRAM_BOT_API = your bot's api key that you get after creating one using BotFather.
    - ACCOUNTS_FILE_NAME = name of the file where you store the accounts' data ("accounts.json" by default)
    - WHITELIST = lits of telegram chat IDs that allowed to receive the steam codes. This is needed to restrict random access. You can also add your friends' ids if they use your accounts.
5. Run the bot with ```python main.py```

Now simply text **/start** to the bot and you should get your steam codes. Enjoy!

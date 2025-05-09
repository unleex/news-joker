# aiogram3-bot-template
This is a template for creating telegram bots based on aiogram3, containing some basic folders and code that can be extended.
# Instructions
## 1. Create  repo 
```bash
git clone https://github.com/unleex/aiogram3-bot-template
```
* go to directory you've just created by cloning
* create your own repository on Github, copy its url and then run the following
```bash
git remote set-url https://github.com/unleex/aiogram3-bot-template; git add .; git push -f
```
## 2. Install all libraries
### Install redis 
Linux: 
    ```bash
    sudo apt install redis-server
    ```
MacOS:
    ```bash
    brew install redis-server
    ```
(https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)

* (optionally to create virtual environment) 
    ```bash
    python -m venv .venv; 
    source .venv/bin/activate
    ```
### Install python libraries
* run 
    ```bash
    pip install -r requirements.txt
    ``` 

## 3. Register your bot
* go to Bot Father and register your bot
* get your bot token from there and paste in .env.example *BOT_TOKEN=\<token>*
* also in .env.example, add wanted user ids to 
*ADMIN_IDS=[\<id1>, \<id2>]* 
(you can add privileges to these users if you want)
* rename .env.example to .env

## 4. Run
* execute ```bash redis-server``` in separate terminal and keep it
## 5. Enjoy!
* replace this README with yours (except for last line please:3)
* extend handlers, lexicon, keyboards or else!
* contact me on Telegram **@unleex** if you want to add something here!

**Please leave the below line for attribution. Thank you!**

*This bot was created using template https://github.com/unleex/aiogram3-bot-template*
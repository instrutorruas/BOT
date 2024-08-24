from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import discord
from discord.ext import tasks, commands
import time
import os
from discord.ext import commands

# Discord bot setup
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Cam4 profile URL
PROFILE_URL = os.getenv('PROFILE_URL')  # Replace 'username' with the actual username

def check_live_status():
    """Check if the profile is live on Cam4."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--window-size=100,100")  # Set a window size to avoid any potential issues
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(PROFILE_URL)
    
    time.sleep(5)  # Wait for the page to load fully
    
    try:
        live_indicator = driver.find_element(By.ID, 'profileVideoWrap')
        driver.quit()
        return live_indicator is not None
    except:
        driver.quit()
        return False

@tasks.loop(minutes=5)  # Check every 5 minutes
async def monitor_cam4():
    channel = bot.get_channel(CHANNEL_ID)
    
    if check_live_status():
        await channel.send(f"{PROFILE_URL} TÁ LIVE CARALHOOOOOOOOOO @everyone")
    else:
        print("Not live")

@bot.event
async def on_ready():
    print(f'Bot is ready. Monitoring {PROFILE_URL}')
    monitor_cam4.start()

# Run the bot
bot.run(TOKEN)

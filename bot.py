from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import discord
from discord.ext import commands
import time
import os

# Discord bot setup
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # Convert to integer
PROFILE_URL = 'https://pt.cam4.com/alicemonteiro' # Replace 'username' with the actual username

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

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

@bot.event
async def on_ready():
    print(f'Bot is ready. Monitoring {PROFILE_URL}')
    
    # Run the live status check once
    channel = bot.get_channel(CHANNEL_ID)
    
    if check_live_status():
        await channel.send(f"{PROFILE_URL} TÁ LIVE CARALHOOOOOOOOOO @everyone")
    else:
        print("Not live")
    
    # Stop the bot after checking
    await bot.close()

# Run the bot
bot.run(TOKEN)

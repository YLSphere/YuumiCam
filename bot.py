import discord
import cv2
import os
import asyncio
import config
import imageio
from discord.ext import commands

bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("YuumiCam is online")
    channel = bot.get_channel(config.CHANNEL_ID)
    await channel.send('YuumiCam is online! Use !help for commands')
    
@bot.command()
async def ping(ctx):
    await ctx.send('Hello human!')

@bot.event
async def on_message(message):
    if message.content.lower() == "!help":
        await send_help_message(message.channel)
    if message.content.lower() == "!cat":
        print('Creating GIF!')
        await create_and_send_gif(message.channel)

async def send_help_message(channel):
    """Send a help message listing all commands."""
    help_message = (
        "**Bot Commands:**\n"
        "`!help` - Show this help message.\n"
        "`!cat` - Capture and send a short GIF of said cat.\n"
    )
    await channel.send(
        help_message,
        allowed_mentions=discord.AllowedMentions.none(), 
        mention_author=False
        )
    
async def create_and_send_gif(channel):
    await channel.send("Downloading cat...")
    cap = cv2.VideoCapture(0)  # Open the webcam
    print(cap)
    if not cap.isOpened():
        await channel.send("Could not access the webcam.")
        return

    frames = []
    frame_count = 120  # Number of frames for the GIF
    fps = 30  # Frame rate for the GIF

    for _ in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame (OpenCV uses BGR, while GIFs need RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame_rgb)

        # Wait a bit between frame captures
        await asyncio.sleep(1 / fps)

    cap.release()

    # Create the GIF
    gif_path = "webcam_output.gif"
    imageio.mimsave(gif_path, frames, format="GIF", fps=fps)

    # Send the GIF to Discord
    await channel.send(file=discord.File(gif_path))

    # Clean up
    os.remove(gif_path)


bot.run(config.BOT_TOKEN)
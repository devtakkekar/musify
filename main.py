import discord
from discord.ext import commands
import yt_dlp
import asyncio
from discord import app_commands
from dotenv import load_dotenv
import os
import platform

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Determine FFmpeg path based on OS
def get_ffmpeg_path():
    if platform.system() == "Windows":
        return "./ffmpeg/ffmpeg.exe"
    else:
        return "./ffmpeg/ffmpeg"  # For Linux/macOS

FFMPEG_EXECUTABLE = get_ffmpeg_path()

# FFmpeg options
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# yt-dlp options
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

async def extract_info(url):
    return await asyncio.to_thread(lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False))

class MusicPlayer:
    def __init__(self):
        self.queue = []  # (url, title)
        self.is_playing = False
        self.current_song = None

    async def play_next(self, voice_client):
        if len(self.queue) > 0:
            self.is_playing = True
            url, title = self.queue.pop(0)
            self.current_song = (url, title)

            try:
                info = await extract_info(url)
                audio_url = info['url']

                voice_client.play(
                    discord.FFmpegPCMAudio(audio_url, executable=FFMPEG_EXECUTABLE, **FFMPEG_OPTIONS),
                    after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(voice_client), bot.loop)
                )
                print(f"Now playing: {title}")
            except Exception as e:
                print(f"Error playing song: {e}")
                self.current_song = None
                await voice_client.disconnect()
                await self.play_next(voice_client)
        else:
            self.is_playing = False
            self.current_song = None

player = MusicPlayer()

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="play", description="Play a song from YouTube")
async def play(interaction: discord.Interaction, url: str):
    if not interaction.user.voice:
        await interaction.response.send_message("You need to be in a voice channel to use this command!")
        return

    voice_channel = interaction.user.voice.channel
    voice_client = interaction.guild.voice_client

    if not voice_client:
        voice_client = await voice_channel.connect()
    elif voice_client.channel != voice_channel:
        await voice_client.move_to(voice_channel)

    await interaction.response.defer()

    try:
        info = await extract_info(url)
        title = info.get('title', url)
        player.queue.append((url, title))
        await interaction.followup.send(f"Added song to queue: {title}")

        if not player.is_playing:
            await player.play_next(voice_client)
    except Exception as e:
        print(f"Error adding song: {e}")
        await interaction.followup.send(f"Could not get info for song: {url}")

@bot.tree.command(name="stop", description="Stop the current song and clear the queue")
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client:
        player.queue.clear()
        player.is_playing = False
        player.current_song = None
        voice_client.stop()
        await interaction.response.send_message("Music stopped and queue cleared.")
    else:
        await interaction.response.send_message("The bot is not in a voice channel.")

@bot.tree.command(name="pause", description="Pause the current song")
async def pause(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await interaction.response.send_message("Music paused.")
    else:
        await interaction.response.send_message("No music is currently playing.")

@bot.tree.command(name="resume", description="Resume the paused song")
async def resume(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await interaction.response.send_message("Music resumed.")
    else:
        await interaction.response.send_message("No music is currently paused.")

@bot.tree.command(name="dc", description="Disconnect the bot from the voice channel")
async def dc(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await interaction.response.send_message("Disconnected from the voice channel.")
    else:
        await interaction.response.send_message("The bot is not in a voice channel.")

@bot.tree.command(name="nowplaying", description="Show the current playing song")
async def nowplaying(interaction: discord.Interaction):
    if player.current_song:
        url, title = player.current_song
        await interaction.response.send_message(f"Now playing: {title}")
    else:
        await interaction.response.send_message("No song is currently playing.")

@bot.tree.command(name="skip", description="Skip the current song")
async def skip(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_playing():
        await interaction.response.send_message("Skipping song...")
        voice_client.stop()
    else:
        await interaction.response.send_message("No song is currently playing to skip.")

@bot.tree.command(name="queue", description="Show the current song and the queue")
async def queue(interaction: discord.Interaction):
    await interaction.response.defer()

    if not player.current_song and not player.queue:
        await interaction.followup.send("The queue is empty.")
        return

    queued_songs_titles = [f"{i+1}. {song[1]}" for i, song in enumerate(player.queue)]
    current_title = player.current_song[1] if player.current_song else "Nothing"
    queued_songs_str = "\n".join(queued_songs_titles) if queued_songs_titles else "Empty"

    queue_message = f"**Now playing:** {current_title}\n\n**Queue:**\n{queued_songs_str}"
    await interaction.followup.send(queue_message)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))

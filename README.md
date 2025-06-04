# Musify - Discord Music Bot

A feature-rich Discord music bot that allows users to play music from YouTube in voice channels. Built with Python using discord.py and yt-dlp.

## Features

- 🎵 Play music from YouTube URLs
- 📋 Queue management system
- ⏯️ Playback controls (play, pause, resume, stop)
- ⏭️ Skip current song
- 📊 View current queue and now playing information
- 🎚️ High-quality audio streaming (192kbps MP3)
- 🔄 Automatic reconnection handling
- 🎧 Cross-platform support (Windows, Linux, macOS)

## Commands

- `/play <url>` - Play a song from YouTube
- `/stop` - Stop the current song and clear the queue
- `/pause` - Pause the current song
- `/resume` - Resume the paused song
- `/skip` - Skip the current song
- `/queue` - Show the current song and queue
- `/nowplaying` - Display the currently playing song
- `/dc` - Disconnect the bot from the voice channel

## Technical Details

- Built with discord.py and yt-dlp
- Uses FFmpeg for audio processing
- Implements slash commands for better user experience
- Handles voice channel connections and disconnections
- Supports high-quality audio streaming
- Includes error handling and reconnection logic

## File Structuring
![image](https://github.com/user-attachments/assets/ac408fbd-cc5b-47a0-9e90-d04c4eadeebc)


## Requirements

- Python 3.8+
- FFmpeg
- discord.py
- yt-dlp
- python-dotenv

## Setup

1. Clone the repository
2. Install required dependencies
3. Set up your Discord bot token in `.env` file
4. Add ffmpeg.exe to the ffmpeg directory according to file structure.
5. Run the bot using `python main.py`

## License

It's free to use.

## Legal Disclaimer

This bot is provided for educational and personal use only. Users are responsible for ensuring they have the right to play the music they request. The bot uses FFmpeg under the LGPL v2.1+ license for audio processing. Please respect copyright laws and YouTube's Terms of Service when using this bot.

The developer(me) of this bot are not responsible for any misuse or copyright infringement by users.

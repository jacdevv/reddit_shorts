# Reddit Shorts
This is Reddit Shorts.

A program that automatically fetches reddit posts, then creates a YouTube short content out of it. It is very easy to use, requiring barely any manual work to make the videos. It can only make 1 video at a time, using 1 background video and multiple background music. The program is very customizable from the terminal.

# How To Use
Inside of the `src` folder there is a sub-folder: Background. Paste a `background` video (under the name *background.mp4*) and a background music (under the name *music.mp3*). Note that you can place more than 1 background music and the program will randomly pick one (name it *music-1.mp3*, *music-2.mp3*, etc. The program automatically counts how many music files there are). If you plan to upload the video to the internet, please use your own content for the background or a fair-use content you downloaded.

After that, create a .env file containing:
- CLIENT_KEY = ... (From Reddit)
- SECRET_KEY = ... (From Reddit)
- SESSION_ID = ... (From TikTok) [How to get it](https://github.com/oscie57/tiktok-voice/wiki/Obtaining-SessionID)

Now that you have a background video, open a terminal inside this folder and run `python main.py`. This will run the script with the default settings. 

Settings:
- `-v` or `--voice`: The code of the desired voice. Default is "en_us_007", [Please check here](https://github.com/oscie57/tiktok-voice/wiki/Voice-Codes).
- `-w` or `--word`: The word count per sentence. Default is 2.
- `-n` or `--name`: The name for the output file (.mp4). Default is "output".
- `-f` or `--font`: The font family for the text. Default is "MontserratBold".
- `-s` or `--subreddit`: The subreddit to fetch data from. Default is "askreddit".
- `-m` or `--mode`: Whether to fetch post or comment. Default is "comment".

Example of a full command: `python main.py -v en_us_007 -w 2 -n output -f MontserratBold -s TrueOffMyChest -m post`.

## Example
[![](https://markdown-videos-api.jorgenkh.no/youtube/9BMwQrbhJHg)](https://youtu.be/9BMwQrbhJHg)

## To-dos
- Create a GUI [Not planned]
- Create a release .exe [Not planned]
---
APIs Used:
- [tiktok-voice by oscie57](https://github.com/oscie57/tiktok-voice)
- [moviepy by Zulko](https://github.com/Zulko/moviepy)
- [whisper by OpenAI](https://github.com/openai/whisper)
- [whisper-timestamped by linto-ai](https://github.com/openai/whisper)
- [praw by Reddit](https://github.com/praw-dev/praw)

Created by [Me](https://github.com/jacdevv)


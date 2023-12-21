from moviepy.editor import *
from moviepy.config import change_settings
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
import threading
import random
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"}) # Path to magick.exe

codec = "libx264" # Codec for the output video
output_file = "output.mp4" # Output file name

def crop_video(background_video):
    # Generate a random number between 1 and 6 (minutes)
    start_time = random.randint(0, 12) * 60  # Convert to seconds

    # Cut the video from the start time to the end
    background_video = background_video.subclip(start_time)

    background_video = background_video.resize(height=1920)
    x_center = background_video.w / 2
    x1 = x_center - 1080 / 2
    x2 = x_center + 1080 / 2
    background_video = background_video.crop(x1=int(x1), y1=0, x2=int(x2), y2=1920)
    return background_video

def create_subtitles(title, background_video, font, comment=None):
    subtitles = []
    delay = 0.8  # Delay in seconds
    max_title_end_time = 0  # To store the end time of the last title subtitle

    # Create title subtitles
    for timestamp, (content, end_time) in title.items():
        start_time = float(timestamp)
        subtitle = TextClip(content, fontsize=80, color='white', method='caption', size=(background_video.w, None), font=f"{font}").set_duration(end_time - start_time).set_start(start_time)
        subtitle = subtitle.set_position(("center", "center"))  # Set the position to center bottom
        subtitles.append(subtitle)
        max_title_end_time = max(max_title_end_time, end_time)

    if comment:
        # Create comment subtitles with delay
        for timestamp, (content, end_time) in comment.items():
            start_time = float(timestamp) + max_title_end_time + delay
            end_time = end_time + max_title_end_time + delay
            subtitle = TextClip(content, fontsize=80, color='white', method='caption', size=(background_video.w, None), font=f"{font}").set_duration(end_time - start_time).set_start(start_time)
            subtitle = subtitle.set_position(("center", "center"))  # Set the position to center bottom
            subtitles.append(subtitle)

    return subtitles

def create_video_with_subtitles(background_video, subtitles):
    # Get the end time of the last subtitle
    last_subtitle_end_time = subtitles[-1].end

    # Create the composite video clip
    video_with_subtitles = CompositeVideoClip([background_video] + subtitles)

    # Set the duration of the video to the end time of the last subtitle
    video_with_subtitles = video_with_subtitles.set_duration(last_subtitle_end_time)

    return video_with_subtitles

def write_output_video(video_with_subtitles, output_file, codec, voice_over):
    video_with_subtitles = video_with_subtitles.set_audio(voice_over)
    video_with_subtitles.write_videofile(output_file, codec=codec, threads=8, fps=30)

def create_video(titleData, output_name, font, background="background/background.mp4", commentData=None):
    print("Building video...")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    background_file_path = os.path.join(dir_path, background)
    background_video = VideoFileClip(background_file_path)  # Open the background video
    background_video = crop_video(background_video)
    if commentData:
        subtitles = create_subtitles(titleData, background_video, font, comment=commentData)
    else:
        subtitles = create_subtitles(titleData, background_video, font)
    video_with_subtitles = create_video_with_subtitles(background_video, subtitles)

    # Load the voice over for title and comment
    voice_file_path_title = os.path.join(dir_path, "title.mp3")
    voice_over_title = AudioFileClip(voice_file_path_title)
    if commentData:
        voice_file_path_comment = os.path.join(dir_path, "comment.mp3")
        voice_over_comment = AudioFileClip(voice_file_path_comment)

    # Load the background music
    music_file_path = os.path.join(dir_path, "background", "music.mp3")
    background_music = AudioFileClip(music_file_path)

    # Cut the first 3 seconds of the background music
    background_music = background_music.subclip(3)

    # Lower the volume of the background music by 50%
    background_music = background_music.volumex(0.5)

    # Get the end time of the last subtitle
    last_subtitle_end_time = subtitles[-1].end

    # Cut the background music to match the video duration
    background_music = background_music.subclip(0, last_subtitle_end_time)

    # Create a 0.8-second silence
    silence = AudioArrayClip(np.zeros((int(0.8 * 44100), 1)), fps=44100)

    # Concatenate the title voice over, silence, and comment voice over
    if commentData:
        voice_over = concatenate_audioclips([voice_over_title, silence, voice_over_comment])
    else:
        voice_over = voice_over_title

    # Combine the voice over and background music
    audio = CompositeAudioClip([voice_over, background_music])

    # Set the audio of the video to the combined audio
    video_with_subtitles = video_with_subtitles.set_audio(audio)

    # Set the duration of the video to the end time of the last subtitle
    video_with_subtitles = video_with_subtitles.set_duration(last_subtitle_end_time)

    # Define the output file path
    output_file = os.path.join(dir_path, "output", f"{output_name}.mp4")

    # Create a separate thread for writing the output video
    output_thread = threading.Thread(target=write_output_video, args=(video_with_subtitles, output_file, codec, audio))
    output_thread.start()
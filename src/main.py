import fetchReddit
import tts
import whisperTimestamp
import transcription
import movie
import os

subreddit = "askreddit"

def main():
    title, comment = fetchReddit.fetch_reddit_data(subreddit)
    tts.create_tiktok_voice(title, comment)

    title = whisperTimestamp.transcribe_audio("title.mp3")
    comment = whisperTimestamp.transcribe_audio("comment.mp3")
    titleData = transcription.convert_words_to_dict(title)
    commentData = transcription.convert_words_to_dict(comment)
    movie.create_video(titleData, commentData, background="background/background.mp4")

    # Delete title.mp3, comment.mp3, and voice.mp3 after its done
    os.remove("title.mp3")
    os.remove("comment.mp3")

if __name__ == "__main__":
    main()

from src import fetchReddit
from src import tts
from src import whisperTimestamp
from src import transcription
from src import movie
import argparse

def process_audio_and_create_video(title, comment, speaker, word_count, output_name, font):
  tts.create_tiktok_voice(title, speaker, comment) 

  title = whisperTimestamp.transcribe_audio("title.mp3")
  if comment:
    comment = whisperTimestamp.transcribe_audio("comment.mp3")
  titleData = transcription.convert_words_to_dict(title, word_count)
  if comment:
    commentData = transcription.convert_words_to_dict(comment, word_count)
  else:
    commentData = None
  movie.create_video(titleData=titleData, commentData=commentData, output_name=output_name, font=font, background="background/background.mp4")

def main(speaker="en_us_007", word_count=2, output_name="output", font="MontserratBold", subreddit="askreddit", mode="comment"):
  if mode == 'post':
    title = fetchReddit.fetch_reddit_data(subreddit, mode)
    if title is None:
      print("No suitable post found.")
      return
    process_audio_and_create_video(title, None, speaker, word_count, output_name, font)
  else:
    title, comment = fetchReddit.fetch_reddit_data(subreddit, mode)
    if title is None or comment is None:
      print("No suitable post or comment found.")
      return
    process_audio_and_create_video(title, comment, speaker, word_count, output_name, font)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create YouTube shorts from Reddit posts")
    parser.add_argument("-v", "--voice", help="The code of the desired voice", default="en_us_007")
    parser.add_argument("-w", "--word", type=int, help="Word count per sentence", default=2)
    parser.add_argument("-n", "--name", help="The name for the output file (.mp4)", default="output")
    parser.add_argument("-f", "--font", help="Font family for the text", default="MontserratBold")
    parser.add_argument("-s", "--subreddit", help="The subreddit to fetch data from", default="askreddit")
    parser.add_argument("-m", "--mode", help="Wether to fetch post or comment", default="comment")
    args = parser.parse_args()

    main(args.voice, args.word, args.name, args.font, args.subreddit, args.mode)

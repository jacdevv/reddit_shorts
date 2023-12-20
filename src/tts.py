import os

SESSION_ID = os.getenv("SESSION_ID")

def create_tiktok_voice(title, comment):
    print("Creating TikTok Voice...")
    
    # Get the directory of this script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Write title to title.txt
    with open(os.path.join(dir_path, "text/title.txt"), "w") as f:
        f.write(title)
    
    # Write comment to comment.txt
    with open(os.path.join(dir_path, "text/comment.txt"), "w") as f:
        f.write(comment)

    # Convert title.txt to title.mp3
    os.system(f"python {os.path.join(dir_path, 'voice.py')} -v en_us_010 -f {os.path.join(dir_path, 'text/title.txt')} --session {SESSION_ID} -n {os.path.join(dir_path, 'title.mp3')}")
    
    # Convert comment.txt to comment.mp3
    os.system(f"python {os.path.join(dir_path, 'voice.py')} -v en_us_010 -f {os.path.join(dir_path, 'text/comment.txt')} --session {SESSION_ID} -n {os.path.join(dir_path, 'comment.mp3')}")

    # Combine title.mp3 and comment.mp3 into voice.mp3 with a 1.5-second delay
    # os.system(f"ffmpeg -y -i {os.path.join(dir_path, 'title.mp3')} -i {os.path.join(dir_path, 'comment.mp3')} -filter_complex \"[1:a]adelay=1000|1000[comment];[0:a][comment]concat=n=2:v=0:a=1\" {os.path.join(dir_path, 'voice.mp3')}")
    # No longer using this method, instead just splice it using moviepy


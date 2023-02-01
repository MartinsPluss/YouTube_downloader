# This program downloads video from YouTube in 1080p and adds 160 kbps audio to it using Ffmpeg installed on OS.
from pytube import YouTube
import os
import subprocess

# Assign YouTube link
yt = YouTube(
    "https://www.youtube.com/watch?v=vSVZrZGm6Mo&t=29s&ab_channel=RedBull")
print('Title:', yt.title)

# Download video in 1080p
video = yt.streams.filter(resolution='1080p', subtype='mp4').first()
video.download(filename='video_1080p.mp4')

# Download audio
audio_stream = yt.streams.filter(only_audio=True, abr='160kbps').first()
audio_stream.download(filename='video_audio.mp3')

video_file = "video_1080p.mp4"
audio_file = "video_audio.mp3"
output_file = "output.mp4"

# Merge video and audio
command = f"ffmpeg -i {video_file} -i {audio_file} -c:v copy -c:a aac {output_file}"
subprocess.run(command.split())

# Delete downloaded temp files
os.remove(video_file)
os.remove(audio_file)


# Rename output, clean filename
def clean_filename(name):
    forbidden_chars = '"*\\/\'.|?:<>'
    filename = (''.join([x if x not in forbidden_chars else '#' for x in name])).replace('  ', ' ').strip()
    if len(filename) >= 176:
        filename = filename[:170] + '...'
    return filename


os.rename(output_file, clean_filename(yt.title) + ".mp4")
print(f'Done - {yt.title} ')

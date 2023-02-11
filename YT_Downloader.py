# CopyRight (c) 2023 Keno Buss
import os
import sys
from pytube import YouTube, Playlist

def remove_invalid_chars(filename):
    invalid_chars = "<>:\"/\\|?*\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
    return "".join(char for char in filename if char not in invalid_chars)


# mp3 download
def download_video_as_mp3(url, save_path):
    yt = YouTube(url)
    audio = yt.streams.get_audio_only()
    filename = remove_invalid_chars(audio.title) + ".mp3"
    audio.download(save_path, filename=filename)

def download_playlist_as_mp3(url, save_path, iterator):
    playlist = Playlist(url)
    video_urls = [video.embed_url for video in playlist.videos]

    for i, video_url in enumerate(video_urls, start=1):
        download_video_as_mp3(video_url, save_path)
        print(f"URL: {iterator}: Audio {i} / {len(video_urls)} is downloaded.")

# mp4 download
def download_video_as_mp4(url, save_path):
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    filename = remove_invalid_chars(video.title) + ".mp4"
    video.download(save_path, filename=filename)

def download_playlist_as_mp4(url, save_path, iterator):
    playlist = Playlist(url)
    video_urls = [video.embed_url for video in playlist.videos]

    for i, video_url in enumerate(video_urls, start=1):
        download_video_as_mp4(video_url, save_path)
        print(f"URL: {iterator}: Video {i} / {len(video_urls)} is downloaded.")



def check_if_single_video_or_playlist (url, path, format, iterator):
    if url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://www.youtu.be/watch?v="):
        if format == "mp3" : download_video_as_mp3(url, path)
        else : download_video_as_mp4(url, path)
    elif url.startswith("https://www.youtube.com/playlist?list=") or url.starstwith("https://youtu.be/playlist?list="):
        if format == "mp3" : download_playlist_as_mp3(url, path, iterator)
        else : download_playlist_as_mp4(url, path, iterator)


def get_urls(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def main():
    # validate and save user inputs
    # Prompt the user for the file path of the URLs
    while True:
        url_file = input("Enter file path of URL .txt Data (each URL in one line): ")
        # Check if the file exists
        if os.path.isfile(url_file):
            break
        print("The file path you entered does not exist. Please try again.")

    # Prompt the user for the save path
    save_path = input("Enter the save folder path : ")
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Prompt the user for the file format
    while True:
        format = input("Do you want to download audio or video files? \n[mp3] audio [mp4] video : ").lower()
        if format == "mp3" or format == "mp4":
            break
        print("Invalid input!\nPlease enter 'mp3' for audio or 'mp4' for video.")

    if not save_path.endswith(os.path.sep):
        save_path += os.path.sep

    urls = get_urls(url_file)

    for i, url in enumerate(urls, start=1):
        try:
            check_if_single_video_or_playlist(url, save_path, format, i)
            print(f"URL {i} / {len(urls)} are downloaded")
        except Exception as e:
            print(f"Something went wrong with URL {i} / {len(urls)}. Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()

# CopyRight (c) 2023 Keno Buss
# Version 1.2
import os
import sys
from pytube import YouTube as YT, Playlist

# #remove invalid chars
def remove_invalid_chars(filename):
    invalid_chars = "<>:\"/\\|?*\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
    return "".join(char for char in filename if char not in invalid_chars)

# download playlist
def download_playlist(url, save_path, iterator, file_type):
    playlist = Playlist(url)
    video_urls = [video.embed_url for video in playlist.videos]

    for i, video_url in enumerate(video_urls, start=1):
        download_stream(video_url, save_path, file_type)
        print(f"URL: {iterator}: Audio {i} / {len(video_urls)} is downloaded.")

# stream download
def download_stream(url, save_path, file_type):
    video = YT(url,use_oauth=True, allow_oauth_cache=True)
    filename = remove_invalid_chars(video.title) + "." + file_type
    
    if file_type == "mp4":
        stream = video.streams.get_highest_resolution()
    elif file_type == "mp3":
        stream = video.streams.get_audio_only()
    
    stream.download(output_path=save_path, filename=filename)

# check is single stream or playlist
def check_if_single_video_or_playlist (url, path, file_type, iterator):
    if url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://www.youtu.be/watch?v="):
        download_stream(url, path, file_type)
    elif url.startswith("https://www.youtube.com/playlist?list=") or url.starstwith("https://youtu.be/playlist?list="):
        download_playlist(url, path, iterator, file_type)

# get urls
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
        file_type = input("Do you want to download audio or video files? \n[mp3] audio [mp4] video : ").lower()
        if file_type == "mp3" or file_type == "mp4":
            break
        print("Invalid input!\nPlease enter 'mp3' for audio or 'mp4' for video.")

    if not save_path.endswith(os.path.sep):
        save_path += os.path.sep

    urls = get_urls(url_file)

    for i, url in enumerate(urls, start=1):
        try:
            check_if_single_video_or_playlist(url, save_path, file_type, i)
            print(f"URL {i} / {len(urls)} are downloaded")
        except Exception as e:
            print(f"Something went wrong with URL {i} / {len(urls)}. Error: {e}", file=sys.stderr)
    print("""
====================================
      All URLs are downloaded.
      Thanks for using me! :)
====================================
    """)

if __name__ == "__main__":
    main()

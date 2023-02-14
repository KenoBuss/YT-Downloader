# CopyRight (c) 2023 Keno Buss
import os
from pytube import YouTube, Playlist
from pydub import AudioSegment


# remove invalid characters from file name
def remove_invalid_chars(input_str):
    # Define a string of valid characters
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "

    # Use a list comprehension to filter out invalid characters
    output_str = "".join(char for char in input_str if char in valid_chars)

    return output_str


# mp3 download
def download_video_as_mp3(url, save_path):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_filename = remove_invalid_chars(audio_stream.default_filename)

    mp3_filename = audio_filename.replace(".mp4", ".mp3")
    mp3_file_path = os.path.join(save_path, mp3_filename)

    # Check if the mp3 file already exists in the save_path
    if os.path.isfile(mp3_file_path):
        return

    # Download the audio stream
    audio_stream.download(save_path, filename=audio_filename)

    # Convert the downloaded audio file to mp3 format
    audio = AudioSegment.from_file(os.path.join(save_path, audio_filename))
    audio.export(mp3_file_path, format="mp3", bitrate="128k")

    # Remove the original audio file
    os.remove(os.path.join(save_path, audio_filename))


def download_playlist(url, save_path, file_type, iterator):
    playlist = Playlist(url)
    video_urls = [video.embed_url for video in playlist.videos]

    for i, video_url in enumerate(video_urls, start=1):
        check_if_single_video_or_playlist(video_url, save_path, file_type)
        print(f"URL: {iterator}: Video {i} / {len(video_urls)} is downloaded.")


# mp4 download
def download_video_as_mp4(url, save_path):
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    filename = remove_invalid_chars(video.title) + ".mp4"
    video.download(save_path, filename=filename)


def is_single_video(url):
    return url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://www.youtu.be/watch?v=")


def is_playlist(url):
    return url.startswith("https://www.youtube.com/playlist?list=") or url.startswith("https://youtu.be/playlist?list=")


def check_if_single_video_or_playlist(url, path, file_type, iterator):
    if is_single_video(url):
        if file_type == "mp3":
            download_video_as_mp3(url, path)
        elif file_type == "mp4":
            download_video_as_mp4(url, path)
        else:
            print(f"Invalid file type: {file_type}")
    elif is_playlist(url):
        download_playlist(url, path, iterator)
    else:
        print(f"Invalid URL: {url}")


def get_urls(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def main():
    # Prompt the user for the file path of the URLs
    default_url_file = "urls.txt"
    url_file = input(f"Enter file path of URL .txt Data (each URL in one line) [{default_url_file}]: ")
    if not url_file:
        url_file = default_url_file
    while not os.path.isfile(url_file):
        print("The file path you entered does not exist. Please try again.")
        url_file = input(f"Enter file path of URL .txt Data (each URL in one line) [{default_url_file}]: ")

    # Prompt the user for the save path
    default_save_path = os.path.join(os.getcwd(), "downloads")
    save_path = input(f"Enter the save folder path [{default_save_path}]: ")
    if not save_path:
        save_path = default_save_path
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if not save_path.endswith(os.path.sep):
        save_path += os.path.sep

    # Prompt the user for the file type
    default_file_type = "mp3"
    file_type = input(f"Do you want to download audio or video files? [mp3] audio / [mp4] video [{default_file_type}]: ").lower()
    if not file_type:
        file_type = default_file_type
    while file_type not in ["mp3", "mp4"]:
        print("Invalid input! Please enter 'mp3' for audio or 'mp4' for video.")
        file_type = input(f"Do you want to download audio or video files? [mp3] audio / [mp4] video [{default_file_type}]: ").lower()

    urls = get_urls(url_file)

    for i, url in enumerate(urls, start=1):
        try:
            check_if_single_video_or_playlist(url, save_path, file_type, i)
            print(f"URL {i} / {len(urls)} is downloaded")
        except Exception as e:
            print(f"Something went wrong with URL {i} / {len(urls)}. Error: {e}")


if __name__ == "__main__":
    main()

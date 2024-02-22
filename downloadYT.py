import time
import threading

from pytube import YouTube
from pytube import Playlist

# Web crawler
import requests
from bs4 import BeautifulSoup

def get_title_from_url(url):
        try:
            # Send a GET request to fetch the web page content
            response = requests.get(url)
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find the <title> tag
            title_element = soup.find('title')
            # Extract the title text
            title = title_element.text.strip()
            return title
        except Exception as e:
            print("Unable to fetch title:", e)
            return None
        
def download_video(video_url, output_path):
    try:
        yt = YouTube(video_url)
        video = yt.streams.get_highest_resolution()
        video.download(output_path)        
    except Exception as e:
        print("Download failed: ", str(e))

def download_youtube_series(playlist_url, output_path): 
    # Playlist
    try:
        playlist = Playlist(playlist_url)
        threads = []
        # Links of all videos in the playlist
        for i, link in enumerate(playlist):
            threads.append(threading.Thread(target=download_video, args=(link, output_path)))
            threads[i].start()
        
        # Wait for all threads to finish downloading
        for i, link in enumerate(playlist):
            threads[i].join()
            youtube_id = get_title_from_url(link)
            print(f"Finished downloading: {youtube_id}")

        print ("All videos downloaded!") 
        return
    
    except Exception as e:
        print("Download failed: ", str(e))
        return

if __name__ == '__main__':

    # Website URL
    input_path = input("Enter the URL: ")
    
    # Create a folder with the title
    title = get_title_from_url(input_path)
    
    start_time = time.time()  # Record the start time

    if "playlist" in input_path:
        playlist_url = input_path
        output_path = title
        download_youtube_series(playlist_url, output_path)
    else:
        video_url = input_path
        output_path = title
        download_video(video_url, output_path)
    
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print("Elapsed Time:", minutes, "minutes", seconds, "seconds")

    
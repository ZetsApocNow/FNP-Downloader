import os
import requests
import re

# Jackett API details
JACKETT_BASE_URL = "ENTER JACKET IP+PORT HERE"
JACKETT_API_KEY = "ENTER JACKET API KEY HERE"
JACKETT_INDEXER = "fearnopeer"

# Download folder
DOWNLOAD_FOLDER = "ENTER DOWNLOAD FOLDER HERE USING \\" #-- Have your torrent program point to this folder to auto-add torrents

# Hardcoded movie folders
MOVIE_FOLDERS = ["ENTER MOVIE FOLDERS HERE USING \\", "ENTER MOVIE FOLDERS HERE USING \\", "ENTER MOVIE FOLDERS HERE USING \\"]

# Video file extensions
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov"]
IGNORED_EXTENSIONS = [".nfo", ".srt"]

def clean_file_name(file_name):
    # Remove the file extension
    cleaned_name = os.path.splitext(file_name)[0]

    # Replace periods with spaces
    cleaned_name = cleaned_name.replace(".", " ").replace("-", " ")

    # Replace the brackets with spaces
    cleaned_name = re.sub(r"\(|\)", " ", cleaned_name).strip()

    # Remove everything from the first 4 digit number to the end
    cleaned_name = re.sub(r"\s\d{4}.*", "", cleaned_name).strip()
    
    cleaned_name = cleaned_name.replace("TVRip", " ").replace("720p", " ").replace("1080p", " ").replace("360p", " ")

    return cleaned_name

def check_local_folders(search_query):
    """
    Check if the requested movie already exists in the local folders, including subfolders.
    Returns a list of matching movie titles.
    """
    matching_titles = []
    for folder in MOVIE_FOLDERS:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for filename in files:
                    if any(filename.endswith(ext) for ext in VIDEO_EXTENSIONS):
                        movie_title = clean_file_name(filename)
                        if movie_title and search_query.lower() in movie_title.lower():
                            matching_titles.append(movie_title)

    return matching_titles

def search_and_save_torrents(search_query):
    """
    Perform a search using the Jackett API and save the raw response to a text file.
    """
    search_url = f"{JACKETT_BASE_URL}/api/v2.0/indexers/{JACKETT_INDEXER}/results/torznab/api?apikey={JACKETT_API_KEY}&t=search&q={search_query}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        
        if not os.path.exists(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER)
        
        results_file_path = os.path.join(DOWNLOAD_FOLDER, "search_results.txt")
        with open(results_file_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        
        # Parse the text file and extract torrent information
        torrents = []
        with open(results_file_path, "r", encoding="utf-8") as file:
            for line in file:
                if "<item>" in line:
                    title = None
                    size_gb = None
                    download_url = None
                    seeders = None
                    
                    while "</item>" not in line:
                        if "<title>" in line:
                            title = line.split("<title>")[1].split("</title>")[0]
                        elif "<size>" in line:
                            size_bytes = int(line.split("<size>")[1].split("</size>")[0])
                            size_gb = size_bytes / 1073741824
                        elif "<link>" in line:
                            download_url = line.split("<link>")[1].split("</link>")[0]
                        elif "<torznab:attr name=\"seeders\"" in line:
                            seeders = int(line.split("value=\"")[1].split("\"")[0])
                        line = next(file)
                    
                    if title and size_gb and download_url and seeders and seeders > 1 and size_gb < 7:
                        torrent = {
                            "title": title,
                            "size_gb": size_gb,
                            "download_url": download_url,
                            "seeders": seeders
                        }
                        torrents.append(torrent)
        
        return torrents
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return []

def download_torrent(download_url, filename):
    """
    Download the torrent file from the provided URL and save it to the download folder.
    """
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        
        download_path = os.path.join(DOWNLOAD_FOLDER, filename + ".torrent")
        with open(download_path, "wb") as file:
            file.write(response.content)
        print(f"\033[94mTorrent downloaded: \033[91m{filename}.torrent\033[0m")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading torrent: {e}")

def main():
    while True:
        print("\033[92mEnter the movie title you want to search for:\033[0m")
        search_query = input()
        if not search_query:
            continue

        local_matches = check_local_folders(search_query)
        if local_matches:
            print("\033[93mMatching files found in local folders:\033[0m")
            for match in local_matches:
                print(f"\033[93m- {match}\033[0m")

            print("\033[92mDo you still want to perform a torrent search? (y/n)\033[0m")
            user_response = input()
            if user_response.lower() == "y":
                results = search_and_save_torrents(search_query)
                if results:
                    print("\033[93mAvailable torrents:\033[0m")
                    for i, torrent in enumerate(results, start=1):
                        print(f"\033[93m{i}. {torrent['title']} - {torrent['size_gb']:.2f} GB - Seeders: {torrent['seeders']}\033[0m")

                    print("\033[92mEnter the number of the torrent you want to download (or press Enter to go back): \033[0m")
                    selection = input()
                    if selection.isdigit() and 1 <= int(selection) <= len(results):
                        selected_torrent = results[int(selection) - 1]
                        download_torrent(selected_torrent["download_url"], selected_torrent["title"])
                        # Return to the initial prompt after downloading the torrent
                        continue
            else:
                # Return to the initial prompt
                continue
        else:
            results = search_and_save_torrents(search_query)
            if results:
                print("\033[93mAvailable torrents:\033[0m")
                for i, torrent in enumerate(results, start=1):
                    print(f"\033[93m{i}. {torrent['title']} - {torrent['size_gb']:.2f} GB - Seeders: {torrent['seeders']}\033[0m")

                print("\033[92mEnter the number of the torrent you want to download (or press Enter to go back): \033[0m")
                selection = input()
                if selection.isdigit() and 1 <= int(selection) <= len(results):
                    selected_torrent = results[int(selection) - 1]
                    download_torrent(selected_torrent["download_url"], selected_torrent["title"])
                    # Return to the initial prompt after downloading the torrent
                    continue
            else:
                print("\033[91mNo torrents found. Please search on the website: \033[93mhttps://fearnopeer.com/torrents\033[0m")
                # Return to the initial prompt
                continue

if __name__ == "__main__":
    main()
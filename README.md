# What is it?

Movie downloader script I made with the help of Claude AI to make my life easier.

## What are the requirements?

Requires Jackett set up running with FearNoPeer added as an indexer

Please do open the py file and edit the  
  
JACKETT_BASE_URL - usually http://localhost:9117  
JACKETT_API_KEY - can be found at the top of the Jackett dashboard  
DOWNLOAD_FOLDER - where you want the torrents downloaded to  
MOVIE_FOLDERS - local movie folders to search through  
  
It can be run by simply double clicking it or starting it via CLI.

## What does it do?

The script asks for a film or tv series name, performs a search locally in the movie folders you set up, also temporary cleaning the search location to enable easier search, if it finds an existing match, then displays as such and asks if you wish to continue the torrent search, if nothing is found then it proceeds to search for the torrents. It'll only display those under 7gb with more than 1 seeder.
It'll list the findings and ask you to choose a number to download. It'll then download the chosen torrent to your set download folder. Here you need to point your torrent program to this folder for auto downloading.
If nothing is found in the torrent search, either the torrent doesn't exist or it does and it's too big, it'll let you know with a link to the website for an enhanced search.
After the download is done, it'll revert back to the original prompt.

You may hit a wall with the downloading if you don't keep seeding old torrents as FNP has a 0.80 ratio policy, this can be mitigated by purchasing VIP.


### Screenshot

![Screenshot 2025-06-04 120344](https://github.com/user-attachments/assets/3cd9ba23-ea40-45ee-ab47-593ec9e851eb)

=====================================================================================

I've also added my optional script for posting to discord a notification of a movie being added, it cleans the name (not 100%) and posts  
"[media name] has been added" into the chosen channel webhook. It checks every 5 seconds and displays "Posted to Discord" in the CLI. Again you need to open the py up and change the below variables.

FOLDER_TO_WATCH  
DISCORD_WEBHOOK  

![Screenshot 2025-06-04 123206](https://github.com/user-attachments/assets/b6f5e2eb-502e-4cb2-84a1-43b5420a481b)

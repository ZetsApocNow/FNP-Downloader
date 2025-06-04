Movie downloader script I made with the help of Claude AI to make my life easier.

Probably requires an account on FearNoPeer and also Jackett set up running.

The script asks for a film or tv series name, performs a search locally in the movie folders you set up, also temporary cleaning the search location to enable easier search, if it finds an existing match, then displays as such and asks if you wish to continue the torrent search, if nothing is found then it proceeds to search for the torrents. It'll only display those under 7gb with more than 1 seeder.
It'll list the findings and ask you to choose a number to download. It'll then download the chosen torrent to your set download folder. Here you need to point your torrent program to this folder for auto downloading.

If nothing is found in the torrent search, either the torrent doesn't exist or it does and it's too big, it'll let you know with a link to the website for an enhanced search.

After the download is done, it'll revert back to the original prompt.

Please do open the py file and edit the JACKETT_BASE_URL, JACKETT_API_KEY, DOWNLOAD_FOLDER, MOVIE_FOLDERS. It can be run by simply double clicking it or starting it via CLI.

![Screenshot 2025-06-04 120344](https://github.com/user-attachments/assets/3cd9ba23-ea40-45ee-ab47-593ec9e851eb)

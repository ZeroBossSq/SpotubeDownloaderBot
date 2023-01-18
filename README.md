# Welcome
## SpotubeDownloaderBot

<p align="center">
    <img src="https://img.shields.io/badge/python-3.10-green?logo=python&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/code-size/ZeroBossSq/SpotubeDownloaderBot?style=for-the-badge">
    <img alt="Website" src="https://img.shields.io/website?down_color=red&down_message=offline&label=status&style=for-the-badge&up_color=blue&up_message=online&url=https%3A%2F%2FSpotifyDownloader.zxbtlkxc.repl.co">
</p>

A small bot written in [pyTelegramBotApi](https://github.com/eternnoir/pyTelegramBotAPI) to download music from spotify or youtube, using a conditional "quick track send" system

## Setup and Dependencies
* Clone the repository:
```
git clone https://github.com/ZeroBossSq/SpotubeDownloaderBot
```

* Install the dependencies:
```
pip install --upgrade pip && pip install -r requirements.txt
```

* Run the bot:
```
python3 -m main.py
```
### Variables

To run this project, you will need to add the following env variables to your env.py file

`MYSQL_HOST` `MYSQL_USER` `MYSQL_PASSWORD` `MYSQL_ROOTPASS` `MYSQL_DATABASE` `SPOTIFY_LOG_CHANNEL_ID` `TELEGRAM_BOT_TOKEN` `SPOTIPY_CLIENT_ID` `SPOTIPY_CLIENT_TOKEN`

## License

This project is under the [MIT license](./LICENSE).

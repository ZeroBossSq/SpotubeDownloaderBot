import os

TOKEN = os.getenv('zwy_spotify_tg_bot')
DB_FN = 'db.sql'
DB_DUMPS = ('CREATE TABLE tracks(full_name TEXT NOT NULL, data BLOB NOT NULL)',)

# telegram
OWNER_ID = 880708503
LOG_CHANNEL_ID = -807746448

# spotify credentials
SPOTIFY_TOKEN = os.getenv('zwy_spotify_tg_bot_spotipy_token')
SPOTIFY_CLIENT_ID = os.getenv('zwy_spotify_tg_bot_spotipy_client_id')

import io
import os
import copy
import sqlite3
import pytube.exceptions
import aiogram
from spotipy.client import Spotify
import funcs
import classes
import settings

spotify_client: Spotify


async def message_handler(message: aiogram.types.Message):
    if 'spotify' not in message.text and 'youtu' not in message.text:
        return

    process_message = await message.reply('⏳')
    status_message = await message.reply('Searching 🔍')

    if 'spotify' in message.text:
        triggered = 'spotify'
        track = classes.SpotifyTrackInfo(spotify_client, message.text)
        track_name = track.full_name

        thumb_bytes_io = io.BytesIO(track.album_images.large.bytes)
        thumb_i_f = aiogram.types.InputFile(copy.copy(thumb_bytes_io))

        await process_message.reply_photo(
            photo=thumb_i_f,
            caption=f'`{track_name}` (duration: {track.duration}m)\n\n'
                    f'(Images: [large]({track.album_images.large.url}), [medium]({track.album_images.medium.url}), [small]({track.album_images.small.url}))',
            parse_mode=aiogram.types.ParseMode.MARKDOWN
        )

        track_name = track.full_name
    else:
        triggered = 'youtube'
        track = pytube.YouTube(message.text)
        track_name = f'{track.title} - {track.author}'

        thumb_bytes_io = await funcs.download_file(track.thumbnail_url)
        thumb_i_f = aiogram.types.InputFile(copy.copy(thumb_bytes_io))

        await process_message.reply_photo(
            photo=thumb_i_f,
            caption=f'`{track_name}` (duration: {track.length / 60:.2f}m)\n\n'
                    f'(Images: [image]({track.thumbnail_url}))',
            parse_mode=aiogram.types.ParseMode.MARKDOWN
        )

    track_in_db = await funcs.search_track_info_in_db(track_name)

    if track_in_db is not None:
        track_fn = await funcs.justify_track_fn(track_name)
        audio_i_f = aiogram.types.InputFile(track_in_db, filename=track_fn)
        thumb_i_f = aiogram.types.InputFile(copy.copy(thumb_bytes_io))

        await status_message.edit_text('Sending ⚙️')
        await status_message.reply_audio(audio_i_f, title=track_name, thumb=thumb_i_f)
        await status_message.edit_text('Done ✅')
        return

    track_fn = f'{await funcs.justify_track_fn(track_name)}.mp3'
    await status_message.edit_text('Downloading 🔰')

    download_track = track
    if triggered == 'spotify':
        download_track: pytube.YouTube = pytube.Search(track_name).results[0]

    if download_track.length > 60 * 5:
        await status_message.reply('The duration of the song you requested is more than 5 minutes! 😖')
        return

    try:
        download_track.streams.get_audio_only().download(filename=track_fn)
    except pytube.exceptions.AgeRestrictedError:
        await status_message.reply('This video is age restricted, i cant download it without be logged in! 😩')
        return

    with open(track_fn, 'rb') as file:
        content = copy.copy(file.read())
    os.remove(track_fn)

    track_bytes_io = io.BytesIO(content)
    track_i_f = aiogram.types.InputFile(copy.copy(track_bytes_io), filename=track_fn)
    thumb_i_f = aiogram.types.InputFile(copy.copy(thumb_bytes_io))

    await status_message.edit_text('Sending ⚙️')
    await status_message.reply_audio(track_i_f, title=track_name, thumb=thumb_i_f)
    await status_message.edit_text('Done ✅ (adding to a db)')

    with sqlite3.connect(settings.DB_FN) as sql:
        cur = sql.cursor()
        cur.execute(f'INSERT INTO tracks (full_name, data) VALUES ((?), (?))', (track_name, track_bytes_io.read()))

    await status_message.edit_text('Done ✅')

import io
import os
import pytube
import aiogram
from spotipy.client import Spotify
import classes
import funcs

spotify_client: Spotify


async def message_handler(message: aiogram.types.Message):
    if 'spotify' not in message.text and 'youtu' not in message.text:
        return

    process_message = await message.reply('⏳')

    if 'spotify' in message.text:
        track = classes.SpotifyTrackInfo(spotify_client, message.text)

        thumb_bytes_io = io.BytesIO(track.album_images.large.bytes)
        thumb_i_f = aiogram.types.InputFile(thumb_bytes_io)

        await process_message.reply_photo(
            photo=thumb_i_f,
            caption=f'`{track.full_name}` (duration: {track.duration}m)\n\n'
                    f'(Images: [large]({track.album_images.large.url}), [medium]({track.album_images.medium.url}), [small]({track.album_images.small.url}))',
            parse_mode=aiogram.types.ParseMode.MARKDOWN
        )

        track_name = track.full_name
    else:
        track = pytube.YouTube(message.text)
        track_name = f'{track.title} - {track.author}'

        thumb_bytes_io = await funcs.download_file(track.thumbnail_url)
        thumb_i_f = aiogram.types.InputFile(thumb_bytes_io)

        await process_message.reply_photo(
            photo=thumb_i_f,
            caption=f'`{track_name}` (duration: {track.length}m)\n\n'
                    f'(Images: [image]({track.thumbnail_url}))',
            parse_mode=aiogram.types.ParseMode.MARKDOWN
        )

    track_fn = f'{await funcs.justify_track_fn(track_name)}.mp3'
    status_message = await message.reply('Downloading 🔰')

    download_track: pytube.YouTube = pytube.Search(track_name).results[0]
    if download_track.length > 60 * 5:
        await status_message.reply('The duration of the song you requested is more than 5 minutes! 😖')
        return

    download_track.streams.get_audio_only().download(filename=track_fn)
    await status_message.edit_text('Sending ⚙️')

    track_file = open(track_fn, 'rb')
    bytes_io = io.BytesIO(track_file.read())
    audio_i_f = aiogram.types.InputFile(bytes_io)

    await status_message.reply_audio(audio_i_f, title=track_name)

    track_file.close()
    os.remove(track_fn)

    await status_message.reply('Done ✅')

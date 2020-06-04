from spotify_interface.get_metadata import get_song_metadata

song_info_string = get_song_metadata()
info_list = song_info_string.split('\n')


def get_length():
    length = info_list[1]
    length = int(length.split('|')[-1])
    length = int(length/1000000)
    seconds = length % 60
    minutes = length//60
    return f"{minutes}:{seconds}"


def get_art_url():
    art_url = info_list[2]
    art_url = art_url.split('|')[-1]
    return art_url


def get_album():
    album = info_list[3]
    album = album.split('|')[-1]
    return album


def get_artist():
    artist = info_list[5]
    artist = artist.split('|')[-1]
    return artist


def get_track():
    track = info_list[8]
    track = track.split('|')[-1]
    return track


def get_URI():
    uri = info_list[-1]
    uri = uri.split('|')[-1]
    return uri


def get_meta_dict():
    meta_dict = {'length': get_length(), 'art_url': get_art_url(), 'album': get_album(), 'artist':  get_artist(), 'track': get_track(), 'uri': get_URI()}
    return meta_dict

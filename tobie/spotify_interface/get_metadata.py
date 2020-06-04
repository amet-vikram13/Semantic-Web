from subprocess import Popen, PIPE


def get_song_metadata():
    metadata_obj = Popen(["./spotify_interface/shell_scripts/sp", "metadata"], stdout=PIPE, stderr=PIPE)
    song_metadata, error = metadata_obj.communicate()
    if metadata_obj.returncode != 0:
        print("No song playing right now")
    elif song_metadata is None:
        print("No song playing right now")
    else:
        return song_metadata.decode('utf-8').strip()

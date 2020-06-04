import subprocess


def display_art(art_url):
    subprocess.run(["./spotify_interface/shell_scripts/display_art", f"{art_url}"])

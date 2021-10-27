import os, glob


def remove_files():
    for f in glob.glob("fragment*.mp3"):
        os.remove(f)

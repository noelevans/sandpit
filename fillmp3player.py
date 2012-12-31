''' 
    Copies music from specified folders (randomly selected) to a media player.
    Usage: 
        python fillmp3player.py /media/mp3mount /data/music1/ /data/music2/
'''
import os
import random
import shutil
import sys

MUSIC_FORMATS = ('mp3', 'wma', 'flac', 'ogg')

def media_paths(roots):
    ''' Generator to return all music files under the roots folders '''
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            media_paths(['%s/%s' % (dirpath, dirname) for dirname in dirnames])
            for filename in filenames:
                if filename.split('.')[-1] in MUSIC_FORMATS:
                    dirpath = dirpath.endswith('/') and dirpath or dirpath + '/'
                    yield dirpath + filename

def run(mp3_mount, media_folders):
    ''' Main function copying music to the media player '''
    try:
        print('Destination: %s' % mp3_mount)
        collection = list(media_paths(media_folders))
        while True:
            idx = random.randint(0, len(collection) - 1)
            filename = collection[idx]
            destination = mp3_mount + filename.split(os.sep)[-1]
            print('%s -> %s' % (filename, destination))
            shutil.copyfile(filename, destination)
            collection.pop(idx)
    except IOError:
        print 'Filled media player. Done.'
    
if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2:])


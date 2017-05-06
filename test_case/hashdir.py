import checksumdir
import sys
import os


def get_dir_hash(directory):
    if os.path.exists(directory):
        return checksumdir.dirhash(directory, 'sha256')
    else:
        return -1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'parameter number error.'
    else:
        path = os.path.join(os.getcwd(), sys.argv[1])
        if not os.path.exists(path):
            print 'path not exists.'
        else:
            print get_dir_hash(path)
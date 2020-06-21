from sys import argv
import os
import hashlib
import platform as pf

block_size = 32 * 1024 * 1024


def go_hash(path, method='md5'):
    hash_method = {
        'md5': hashlib.md5,
        'sha': hashlib.sha1,
        'sha1': hashlib.sha1,
        'sha224': hashlib.sha224,
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha384,
        'sha512': hashlib.sha512,
        'sha3224': hashlib.sha3_224,
        'sha3256': hashlib.sha3_256,
        'sha3384': hashlib.sha3_384,
        'sha3512': hashlib.sha3_512,
        'blake2b': hashlib.blake2b,
        'blake2s': hashlib.blake2s
    }
    method = method.lower()
    try:
        with open(path, 'rb') as the_file:
            hasher = hash_method[method]()
            end_index = the_file.seek(0, 2)
            the_file.seek(0, 0)
            while the_file.tell() < end_index:
                block = the_file.read(block_size)
                hasher.update(block)
            return hasher.hexdigest()
    except:
        return 'error'


def hash_dir(path, method='md5'):
    is_windows = pf.uname().system == 'Windows'
    slash = '\\' if is_windows else '/'
    prefix = '.' + slash
    if path[-1:] != slash:
        path += slash

    for root, dirs, files in os.walk(path, topdown=True):
        for filename in files:
            current_path = ('{0}{1}{2}' if root[-1:] != slash else '{0}{2}').format(root, slash, filename)
            hash_hex = go_hash(current_path, method)
            print("%s %s" % (hash_hex, current_path.replace(path, prefix, 1)))


def hash_file(path, method='md5'):
    print("%s %s" % (go_hash(path, method), path))


def valid_path(path):
    return os.path.exists(path)


def is_file(path):
    return os.path.isfile(path)


if __name__ == '__main__':
    hash_path = "."
    hash_method = "md5"
    try:
        hash_path = argv[1]
        hash_method = argv[2]
    except:
        pass

    if not valid_path(hash_path):
        exit(233)

    if is_file(hash_path):
        hash_file(hash_path, hash_method)
    else:
        hash_dir(hash_path, hash_method)

    input('Done!')

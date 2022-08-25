import base64
import time
import os
import zipfile


def encode_to_base_64(file_path):
    with open(file_path, "rb") as f:
        bytes = f.read()
        encoded = base64.b64encode(bytes)
        return encoded.decode('utf-8')


def create_path_is_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def check_path_exists(path, mk='zip'):
    path_to_zip = f'{path}\\{mk}\\'
    create_path_is_not_exists(path_to_zip)
    return path_to_zip


def make_zip(path):
    new_zip = zipfile.ZipFile(f'{check_path_exists(path)}{int(time.time())}.zip', 'w')

    for folder, subfolders, files in os.walk(path):
        for file in files:
            if file.endswith(('.jpeg', '.jpg')):
                new_zip.write(
                    os.path.join(folder, file),
                    os.path.relpath(os.path.join(folder, file), path),
                    compress_type=zipfile.ZIP_DEFLATED
                )

    new_zip.close()
    return encode_to_base_64(new_zip.filename)

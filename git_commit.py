import os
import hashlib
from update_library_version import update_version


def update_toml():
    start_hash = hashlib.md5(open('pyproject.toml', 'rb').read()).hexdigest()
    update_version()

    if start_hash != hashlib.md5(open('pyproject.toml', 'rb').read()).hexdigest():
        return True


def start():
    if update_toml() is True:
        os.system('git add .')
        os.system(f'git commit -m "{input("Напиши текст коммита: ")}"')
        os.system('git branch -M raifazen')
        os.system('git push -u origin raifazen')


if __name__ == '__main__':
    start()

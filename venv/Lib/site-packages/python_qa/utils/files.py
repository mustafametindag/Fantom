import os
import random as rnd


def bytes_to_file(file_path: str, data: bytes) -> None:
    with open(file_path, 'wb') as binary_file:
        binary_file.write(data)


def choice_file(path: str):
    path = path if path[-1] == "/" else path + "/"
    return path + rnd.choice(os.listdir(path))

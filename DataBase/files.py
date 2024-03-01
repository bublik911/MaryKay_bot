import os
from pathlib import Path

from dotenv import load_dotenv

from aiogram.types import Message

from repositories import ConsultantRepository

load_dotenv()


def create_directories():
    os.chdir(str(Path.home()))
    if not os.path.isdir(os.getenv("FILE_STORAGE")):
        os.mkdir(os.getenv("FILE_STORAGE"))

    os.chdir(os.getenv("FILE_STORAGE"))
    consultants = ConsultantRepository.get_all_consultants_chat_id()

    for chat_id in consultants:
        if not os.path.isdir(str(chat_id.chat_id)):
            os.mkdir(str(chat_id.chat_id))
            os.chdir(str(chat_id.chat_id))
            os.mkdir("all")
            os.mkdir("birthday")


def get_photo_for_all_message(chat_id: int):
    os.chdir(str(Path.home()))
    os.chdir(os.getenv("FILE_STORAGE"))
    os.chdir(str(chat_id))
    os.chdir("all")
    list = os.listdir()
    path_list = []
    for path in list:
        path_list.append(os.path.abspath(path))
    return path_list


def get_photo_for_birthday_message(chat_id: int):
    os.chdir(str(Path.home()))
    os.chdir(os.getenv("FILE_STORAGE"))
    os.chdir(str(chat_id))
    os.chdir("birthday")
    list = os.listdir()
    path_list = []
    for path in list:
        path_list.append(os.path.abspath(path))
    return path_list


def download_photo_path(message: Message, specify: str):
    path = path_to_download(message)
    if specify == "all":
        path += "/all"
    elif specify == "birthday":
        path += "/birthday"
    path += "/" + message.photo[-1].file_unique_id + '.jpg'
    return path


def clear_photos(message: Message, specify: str):
    path = path_to_download(message)
    if specify == "all":
        path += "/all"
    elif specify == "birthday":
        path += "/birthday"
    os.chdir(path)
    files = os.listdir()
    for file in files:
        os.remove(file)


def path_to_download(message: Message) -> str:
    os.chdir(str(Path.home()))
    os.chdir(os.getenv("FILE_STORAGE"))
    os.chdir(str(message.chat.id))
    return os.getcwd()


if __name__ == "__main__":
    create_directories()

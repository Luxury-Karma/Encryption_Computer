import re
import subprocess
import os
import main



def traverse_files(start_path):
    with open('.\\folders.txt','w') as save:
        for root, dirs, files in os.walk(start_path):
            for file in files:
                file_path = os.path.join(root, file)
                print(file_path)
                save.write(str(f'{file_path}\n'))


if __name__ == "__main__":
    starting_directory = "C:\\"
    traverse_files(starting_directory)
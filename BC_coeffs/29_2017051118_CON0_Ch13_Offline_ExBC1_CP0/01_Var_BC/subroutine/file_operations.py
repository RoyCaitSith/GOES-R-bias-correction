import os
import sys
import shutil
import re

# Check whether the folder exists. If exists, quit. If not, create it.
def create_new_case_folder(dir_name):
    if os.path.exists(dir_name):
        print(dir_name + ' exists! Quit!')
        #os._exit(0)
    else:
        print(dir_name + ' does not exist! Create it!')
        os.mkdir(dir_name)

# Copy the files from one folder to another folder
def copy_files(out_folder_dir, in_folder_dir):
    for root, dirs, files in os.walk(out_folder_dir, topdown = False):
        for flnm_dir in files:
            shutil.copy(os.path.join(root, flnm_dir), in_folder_dir)

# Change the content in a txt file
class change_content:

    def __init__(self, path):
        self.path = path
        temp = open(path)
        self.content = temp.readlines()
        temp.close()
        for idx, item in enumerate(self.content):
            self.content[idx] = item.lstrip()
            if self.content[idx] == '':
                self.content[idx] = '\n'
            if re.match('mpirun', self.content[idx]):
                self.content[idx] = '\n'
            if re.match('exit 0', self.content[idx]):
                self.content[idx] = '\n'
        idx = len(self.content)-1
        while self.content[idx] == '\n':
            self.content.pop()
            idx = idx-1

    def substitude_string(self, var_name, flag, sub_content):
        for idx, item in enumerate(self.content):
            if re.match(var_name, item):
                self.content[idx] = var_name + flag + sub_content + " \n"

    def sub_whole_string(self, judge_content, sub_content):
        for idx, item in enumerate(self.content):
            if re.search(judge_content, item):
                self.content[idx] = sub_content

    def add_string(self, add_content):
        self.content.append(add_content)

    def show_variable(self, var_name):
        for item in self.content:
            if re.match(var_name, item):
                print(item)

    def print_content(self):
        for item in self.content:
            print(item)

    def save_content(self):
        temp = open(self.path, 'w')
        for idx in range(len(self.content)):
            self.content[idx] = self.content[idx].replace('\$', '$')
            temp.write(self.content[idx])
        temp.close()

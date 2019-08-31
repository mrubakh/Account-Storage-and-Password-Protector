from tkinter import *
from tkinter import messagebox
import tkinter.messagebox
import base64
import os
import itertools
import json
import io
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from collections import OrderedDict

# Globals

os.chdir('C:/Users/Mark/Documents/College/Password Protector')
window = Tk()
window.withdraw()
window.title('Account Storage')
accounts = []
max_attempts = 3
current_user = ''
total_count = 0

#Creates the starting password window
class Window_Start(object):

    loop = False
    attempts = 0

    def __init__(self, master):
        self.top = Toplevel(master=master)
        self.top.title("Enter Info")
        self.top.geometry("{}x{}".format(300,120))
        self.top.resizable(width=False, height=False)
        self.user_label = Label(self.top, text=" Username: ", font=('Bookman',14)).grid(row=3)
        self.pass_label = Label(self.top, text=" Password: ", font=('Bookman',14)).grid(row=4)
        self.user_entry = Entry(self.top, width=25)
        self.user_entry.grid(row=3, column=2)
        self.pass_entry = Entry(self.top, show="*",width=25)
        self.pass_entry.grid(row=4, column=2, padx=3)
        self.sub_button = Button(self.top, text='Submit',command=self.entry_access, font=('Bookman',14))
        self.sub_button.grid(columnspan=2, sticky=W, row=5, column=1)

    #Starts the main window after password authentication
    def start_main_window(self,curr_user):
        global current_user
        current_user = curr_user
        welcome_label = Label(window, text='Welcome {}!'.format(current_user.capitalize()), font=('Bookman',18))
        welcome_label.grid(columnspan=6, column=0, padx=5, row=0)
        readfile()
        self.loop = True
        self.top.destroy()
        window.deiconify()

    #checks if the username or password is left blank
    def user_or_pass_blank(self):
        return len(self.user_entry.get()) < 1 or len(self.pass_entry.get()) < 1

    #either verifies the account or creates a new account if the username does not exist
    def verify_or_create(self, entry_exists, all_users, flattened_list, curr_user):
        with open('master_data.json', 'w') as master_data:
            if entry_exists:
                current_pass = remove_encryption(all_users[flattened_list.index(curr_user)])[1]
                json.dump(all_users, master_data)
                if self.pass_entry.get() == current_pass:
                    self.start_main_window(curr_user)
                else:
                    self.attempts += 1
                    if self.attempts == max_attempts:
                        window.quit()
                    self.pass_entry.delete(0,'end')
                    messagebox.showerror('Incorrect Password',
                    'Incorrect password, attempts remaining: {}'.format(str(max_attempts - self.attempts)))
            else:
                new_encryption = create_encryption(curr_user, self.pass_entry.get())
                all_users.append(new_encryption)
                json.dump(all_users, master_data)
                self.start_main_window(curr_user)

    #authentication helper function
    def entry_access(self):
        entry_exists = False
        all_users = []
        curr_user = self.user_entry.get().strip()
        if self.user_or_pass_blank():
            messagebox.showerror("Username or Password Missing", "Username or Password cannot be blank.")
            return
        print(self.user_or_pass_blank())
        try:
            mode = 'w+' if not os.path.isfile('master_data.json') else 'r'
            with open('master_data.json', mode) as master_data:
                if mode == 'r':
                    all_users=json.load(master_data)

                list_of_entries = list(map(remove_encryption, [dict for dict in all_users]))
                flattened_list = list(itertools.chain.from_iterable(list_of_entries))[::2]
                entry_exists = curr_user in flattened_list #True if the user already has an "account", false otherwise
                self.verify_or_create(entry_exists, all_users, flattened_list, curr_user)
        except PermissionError:
            messagebox.showerror("Permission Denied", "You do not have the correct file permissions")


class Account:
    def __init__(self, master, title, username, password, count, is_new_account):
        self.window = master
        self.title = title
        self.username = username
        self.password = password
        self.count = count
        self.is_new_account = is_new_account

    #encrypts the account and saves it to memory
    def encrypt_account(self):
        all_account = []
        filename = '{}_user.json'.format(current_user)
        encrypted_dict = create_encryption(self.title, self.username, self.password)
        with open(filename, 'r') as account_info:
            if not os.stat(filename).st_size == 0:
                all_account=json.load(account_info)
        with open(filename, 'w') as account_info:
            if self.is_new_account:
                all_account.append(encrypted_dict)
            json.dump(all_account, account_info)

    #displays the account on the main window
    def display(self):
        self.label_title = Label(self.window, text=self.title, font=('Bookman',14))
        self.label_title.grid(row=9 + self.count, sticky=W)
        self.label_username = Label(self.window, text=self.username, font=('Bookman',14))
        self.label_username.grid(row=9 + self.count, column=1)
        self.label_password = Label(self.window, text=self.password, font=('Bookman',14))
        self.label_password.grid(row=9 + self.count, column=2, sticky=E)
        self.delete_button = Button(self.window, text='X', fg='red', command=self.delete_account)
        self.delete_button.grid(row=9 + self.count, column=3, sticky=E)

    #deletes an account if the delete button is pressed
    def delete_account(self):
        answer = tkinter.messagebox.askquestion('Delete', 'Are you sure you want to delete this account?')
        if answer == 'yes':
            filename = '{}_user.json'.format(current_user)
            with open(filename, 'r') as account_info:
                account_list = json.load(account_info)
            with open(filename, 'w') as account_info:
                del account_list[self.count]
                json.dump(account_list, account_info)

            for account in accounts:
                account.destroy()
            global total_count
            total_count = 0
            readfile()

    #destroys all attributes of an account
    def destroy(self):
        self.label_title.destroy()
        self.label_username.destroy()
        self.label_password.destroy()
        self.delete_button.destroy()

#Functions

#creates an instance of an Account object
def create_account(window, title_val, username_val, password_val, is_new_account):
    global total_count
    a = Account(window, title_val, username_val, password_val, total_count, is_new_account)
    accounts.append(a)
    a.encrypt_account()
    a.display()
    total_count += 1

#Account helper object, which also deletes the previous text from the account submission
def submit_entry(window, title, username, password, is_new_account):
    create_account(window, title.get(), username.get(), password.get(), is_new_account)
    title.delete(0, 'end')
    username.delete(0, 'end')
    password.delete(0, 'end')

#returns a dictionary where each key is the encrypted arg, and each value is its respective key --> {encyrpted arg: encrypted arg key}
def create_encryption(*args):
    args_dict= OrderedDict()
    for arg in args:
        provided_entry = arg
        hashed_entry = provided_entry.encode() #converts to bytes
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm = hashes.SHA256,
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        key = base64.urlsafe_b64encode(kdf.derive(hashed_entry))
        f = Fernet(key)
        message = arg.encode()
        encrypted = f.encrypt(message)
        args_dict[encrypted.decode()] = key.decode()
    return args_dict

#takes a key:value pair -->{encyrpted arg: encrypted arg key} and returns a list of the decrypted args
def remove_encryption(encrypted_dict):
    decrypted_list = []
    for item in encrypted_dict:
        key = encrypted_dict[item].encode()
        f = Fernet(key)
        decrypted = f.decrypt(item.encode())
        decrypted_list.append(decrypted)
        final_list = [item.decode() for item in decrypted_list]
    return final_list

#reads and creates instances of stored accounts from the json file
def readfile():
    account_list = []
    filename = '{}_user.json'.format(current_user)
    mode = 'w+' if not os.path.isfile(filename) else 'r'
    with open(filename, mode) as account_info:
        if not os.stat(filename).st_size == 0:
            account_list = json.load(account_info)


        for dict in account_list:
            account_split = remove_encryption(dict)
            create_account(window, account_split[0],account_split[1],account_split[2], False)

def main():
    m = Window_Start(window)
    entity_label = Label(window, text='Add Account',fg='blue', font=('Bookman',14))
    empty_label = Label(window)
    title_label = Label(window, text='Title: ', font=('Bookman',14))
    username_label = Label(window, text='Username: ', font=('Bookman',14))
    password_label = Label(window, text='Password: ', font=('Bookman',14))
    title = Entry(window, font=('Bookman',12), width = 30)
    username = Entry(window, font=('Bookman',12), width = 30)
    password = Entry(window, show='*',font=('Bookman',12), width = 30)
    submit = Button(window, text=" + ", fg='blue',
    command = lambda: submit_entry(window, title, username, password, True), font=('Bookman',14))

    empty_label.grid(columnspan=3, row=1)
    entity_label.grid(columnspan=10, padx=10, row=2)
    title_label.grid(row=3, sticky=E, padx=3)
    username_label.grid(row=4, sticky=E, padx=3)
    password_label.grid(row=5, sticky=E, padx=3)

    title.grid(columnspan=5, row=3, column=1, padx=2, pady=4, sticky=W)
    username.grid(columnspan=5, row=4, column=1, padx=2, pady=4, sticky=W)
    password.grid(columnspan=5, row=5, column=1, padx=2, pady=4, sticky=W)
    submit.grid(columnspan=5, pady=4)

    second_title = Label(window, text='Title: ', font=('Bookman',14))
    second_username = Label(window, text='Username: ', font=('Bookman',14))
    second_password = Label(window, text='Password: ', font=('Bookman',14))

    second_title.grid(row=7)
    second_username.grid(row=7, column=1)
    second_password.grid(row = 7, column=2)

    window.mainloop()

if __name__ == "__main__":
    main()

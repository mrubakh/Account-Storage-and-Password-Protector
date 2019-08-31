# Account-Storage

## Introduction

Nowadays, it's often very difficult to keep track of the vast number of passwords we're required to keep track of on a daily basis. With the growing popularity of the internet, many daily business, political, and social operations require the public to go to a site and create an account with a username and password. Unfortunately, our growing online presence has also given way for many malicious hackers to steal sensitive information from many of these sites. Hacking has gotten so severe that many web services now require certain complexities within a password, making it even MORE difficult for people to remember. To help aleviate this issue, I have created an Account Storage executable program that dynamically stores account information such as title, username, and password in encrypted JSON files which permanently store the account information so long as the JSON files are not tampered with. I have added in functionality to where **multiple users can store account information at the same time, which means that different users will not be able to see each other's account information.**

Since I began this project mostly from scratch (with some slight inspiration from [Tech With Tim's](https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg?&ab_channel=TechWithTim) fantastic Tkinter YouTube series), this project took me over 20 hours to complete, and there is still lots of work that can be done.

## Instructions:

After downloading the passwordprotector.pyw executable, the startup screen will popup. It will prompt you for a username and password as such. 

![Screenshot (26)](https://user-images.githubusercontent.com/33610797/64069732-e59e8580-cc1d-11e9-8ad7-7eb0ceb2d9f4.png)

Unlike most online account registrations, you will **NOT** need to explicitly create a user account in a seperate screen. Simply:
1. Type in a username that does not yet exist in the system
2. Type a password for that username, and you will be brought to the next screen

**It's important to note that no one will be able to see your account information without knowing both your username and password at the starting screen.** If they enter the incorrect password with the selected username, it will give them only two more attempts before the executable shuts down.
 
Once you've entered the correct credentials, you will be brought to the main screen:

![Screenshot (27)](https://user-images.githubusercontent.com/33610797/64069733-f222de00-cc1d-11e9-8184-9233d0d74bfc.png)

Here, you can add an Account "Title", an Account "Username" (which could be an email address, phone number, etc.), and a "Password". This will then be automatically displayed, and then stored in the JSON file corresponding to the username you selected. At any time, you can also delete any Account by clicking the red "X" on the righthand side.

## Encryption Methods / Security

This program uses a symmetric encryption library in Python called Fernet. This means that every entry is given a key used to encrypt and decrypt the entry, so only those who have access to the key and perform the correct cryptographic computation can retreive the original entry. This is done by generating a key based off of any message (for simplicity, I chose the same message that was to be encrypted) which gives the key a value of a URL safe base64 encoded key. From here, all entries must be converted in UTF-8 when performing operations, and back into strings when displayed. For more info, go and read the [Fernet documentation](https://cryptography.io/en/latest/fernet/), which is surprisingly intuitive!

While Fernet itself is an implementation of Advanced Encryption Standard (AES), a standard of encryption established by the National Institute of Standards of Technology, **this basic program is still incredibly susceptible to hackers and can have disasterous effects if used improperly**. However, it is considerably better than storing passwords in plain text files, which no one should ever do! For increased security, I would recommend storing the executable in a password-protect-folder, to further reduce the risk of any information leaks.



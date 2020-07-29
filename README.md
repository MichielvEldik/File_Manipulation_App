# Michiel_Advanced_Project
From Febuary to June I was involved in 'Programming with Python Learning Community Advanced track'. 
This is an extracurricular activity at the university to get acquainted with Python and software development.
We had to construct software that could handle files and perform certain manipulations to them. 
It was up to us to come up with useful functions for the software.

User's guide

***Dependencies / requirements***

I designed this program using:

--> pycrypto 2.6.1 (latest version)
--> Pillow 7.2.1 (latest version)
--> Python 3.8 

Please boot the program from the AA_Main_Menu.py file.

## (0) Introduction

This guide will be kept brief because a lot of explanation is provided within the code itself using doc strings and comments. While reading this guide, please refer to the picture 'program_structure.png' in the current directory. The colours indicate the class in which the options / functions are present. E.g., encryption, decryption and locking files (so they are un-deletable) are separate objects while delete file, rename file, and preview file are kept at the file manipulation menu level.


## (1) Main Menu 

Upon booting the program, the user is confronted with all files and directories within the current directory. When one makes adjustments to files (e.g., renaming or deleting them), changes will only appear after using the "REFRESH BUTTON". However, the possible FileNotFoundErrors associated with trying to manipulate an altered file before hitting the refresh button are accounted for in the program. 

The main menu also keeps track of all deleted files during the session. They will appear in a listbox beneath all of the buttons. Their cumulative bytes are displayed in the entry box above the list. When the user hits the refresh button, this list will disappear. This is a limitation I have tried to fix by keeping a list of deleted file outside of the Tkinter Window. Due to time constraints, I did not finish this yet.

The locked_files.csv is also accessible from the main menu. This is a csv file that contains all file paths that are not to be deleted. 

## (2) Sub directory 

The program deals with sub directories via a dedicated class for this. The class will actually call itself if you are dealing with a directory in a directory of a directory... etc. At some point through your sub directory "rabbit hole" you might want to manipulate a file. This will launch the file manipulation class with all the necessary arguments to make that work smoothly. 

## (3) File Manipulation

### (3.1.) Locking files and deleting files

This is where the interesting things happen. The program_structure.png summaries the functionalities. Because the file manipulation class is always passed the path to the locked_files.csv, locking files is easily done. Before deleting files, the locked_files.csv will be checked if there are any matches. 

### (3.2.) Encryption and Decryption

Furthermore, the user can encrypt and decrypt files. Encryption will generate an AES 128-bit encrypted version of your text or csv files and place it in the current directory. It does so using a key I generated. This same key is defined in the Decryption class to decrypt an encrypted file. It would be far more secure to provide the user with a randomly generated key per file and have him enter it during decryption. However, due to time constraints I have not gotten around to it. Still, if two users were to have this program on their computer, they could safely send each other encrypted files and anyone who intercepts will have a very difficult time decrypting it manually. So there is potential use in it. 

A second limitation is the ~ max 1200 bytes file limit. Messages should be small or split up.It would be fun to write an additional functionality to do this splitting but again... time constraints.

### (3.3) Renaming files

The coding behind this functionality is actually more extensive than one might think. It checks for double names in the directory. It also makes sure that no illegal characters are used. When your press rename file, you get to enter the new name (excluding format extensions) in the second entry box. Then, you use the button 'rename' to actually go through with renaming it. For some reason, on MACOS the colours for buttons don't work whilst they do work on Windows. So the buttons is not as vivid for MAC users.    

### (3.4) Preview files

This functionality can preview almost any kind of image format. It can also preview text files and even csv files. One drawback is that paragraphs are still separated by '{}' and that the user can't scroll through larger images. However, due to time constraints and my perceived importance of these functionalities for a mere preview method has led me to leave this for now. In my opinion, it is sufficient that one can see the text and images so that one has a rough idea of what file he or she is working with.

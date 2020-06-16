from tkinter import *
import os
import csv
from os.path import getsize
from AF_Lock_List import LockList
from AD_Encrypt import Encryption
from AE_Decrypt import Decryption
from PIL import ImageTk, Image, UnidentifiedImageError


class FileManipulation(Frame):
    """Handling Individual Files

    Firstly, the arguments that were passed to the parameters are initialized. Secondly, the files size is retrieved
    using the current_file_location variable. Thirdly, a pop-up window including an entry widget is created. Fourthly,
    Labels for file size and name are packed to the pop-up window. Lastly, the pop-up menu is filled with buttons
    that call various file manipulation methods.

    """
    def __init__(
            self, master=None,
            col_number=None,
            current_file_location=0,
            current_directory_path=0,
            locked_file_location=0
                ):
        """Initialization

        :param master: inherent the root
        :param col_number: The name of the selected file that will be manipulated
        :param current_file_location: The path of the selected file that will be manipulated
        :param current_directory_path: The path to directory in which the selected file is located
        :param locked_file_location: The location of the un-deletable file csv in the 'original' directory

        """

        # initialize frame
        Frame.__init__(self, master=master)

        # initialize root window
        self.master = master

        # initialize variables
        self.col_number = col_number
        self.current_file_location = current_file_location
        self.current_directory_path = current_directory_path
        self.locked_file_location = locked_file_location
        self.file_size_int = getsize(str(self.current_file_location))

        # Import main menu
        from AA_Main_Menu import MenuGui

        # Create pop-up menu with entries
        self.popup = Toplevel()
        self.e = Entry(self.popup)
        self.e.pack(side=TOP, expand=True, fill=BOTH)
        self.e_two = Entry(self.popup)
        self.e_two.pack()
        self.popup.title(str(col_number))
        self.popup.grab_set()

        # Create file size and file name labels
        Label(
            self.popup, text="File name: {}".format(col_number)
            ).pack(side=TOP, expand=True, fill=BOTH)
        Label(
            self.popup, text="File size: {} bytes".format(str(self.file_size_int))
            ).pack(side=TOP, expand=True, fill=BOTH)

        # Create buttons for file manipulations
        Button(
            self.popup, text ="Encrypt file", command=lambda: self.encrypt_file()
            ).pack(side=TOP, expand=True, fill=BOTH)
        Button(
            self.popup, text="Decrypt file", command=lambda: self.decrypt_file()
            ).pack(side=TOP, expand=True, fill=BOTH)
        Button(
            self.popup, text="Lock file (so it can't be deleted)", command=lambda: self.lock_file()
            ).pack(side=TOP, expand=True, fill=BOTH)
        Button(
            self.popup, text="Delete file.", command=lambda: self.delete_current_file(MenuGui)
            ).pack(side=TOP, expand=True, fill=BOTH)
        Button(
            self.popup, text="preview", command=lambda: self.preview()
            ).pack(side=TOP, expand=True, fill=BOTH)
        Button(
            self.popup, text="rename file", command=lambda: self.rename_file()
        ).pack(side=TOP, expand=True, fill=BOTH)

        Button(
            self.popup, text="Return.", command=lambda: self.return_to_main()
            ).pack(side=TOP, expand=True, fill=BOTH)

    def encrypt_file(self):
        """Preparing to launch the Encryption class

        Firstly, the file size is checked. Encryption works only with smaller file sizes. Secondly, an instance of the
        Encryption class is initialized with the following parameters:

            (1) self.current_file_location {str} =  The full path of the file that will be encrypted;
            (2) self.current_directory_path {str} = The path to directory in which the selected file is located;
            (3) self.col_number {str} = The name of the file to be encrypted.

        """
        if self.file_size_int > 1200:
            self.e.delete(0, END)
            self.e.insert(0, "File must be < 1200 bytes!")
        else:
            try:
                f = open(self.current_file_location, 'r')
                plain_text_file = f.read()
                Encryption(self.current_file_location, self.current_directory_path, self.col_number, plain_text_file)
                self.e.delete(0, END)
                self.e.insert(0, "Encrypted successfully!")
            except UnicodeDecodeError:
                self.e.delete(0, END)
                self.e.insert(0, "Can't encrypt this format.")
            except ValueError:
                self.e.delete(0, END)
                self.e.insert(0, "Can't encrypt this format.")
            except FileNotFoundError:
                self.e.delete(0, END)
                self.e.insert(0, "File couldn't be found.")

    def decrypt_file(self):
        """Preparing to launch the Decryption class

        The Decryption class is programmed to turn encrypted binary files back into text files. Thus, anything other than
        such files will eventually cause a ValueError. It takes the following parameters:

            (1) self.current_file_location {str} =  The full path of the file that will be decrypted;
            (2) self.current_directory_path {str} = The path to directory in which the selected file is located;
            (3) self.col_number {str} = The name of the file to be decrypted.

        """
        try:
            f = open(self.current_file_location, 'rb')
            binary_file = f.read()
            Decryption(self.current_file_location, self.current_directory_path, self.col_number, binary_file)
            self.e.delete(0, END)
            self.e.insert(0, "Decrypted successfully!")
        except ValueError:
            self.e.delete(0, END)
            self.e.insert(0, "this format is not supported.")
        except FileNotFoundError:
            self.e.delete(0, END)
            self.e.insert(0, "File couldn't be found.")

    def lock_file(self):
        """Managing file paths of un-deletable files

        This method firstly checks if a new csv files for storing un-deletable file paths is necessary. If not, it
        proceeds to launch the 'append_lock_list' method of the 'imported LockList class'. Otherwise, it will create a
        new csv file in the 'original' directory.

        """
        try:
            with open(self.locked_file_location, 'r', newline='') as r:
                reader = csv.reader(r)
                read_locked_list = list(reader)
                append_lock_list = LockList(self.locked_file_location, self.current_file_location)

                # append_locklist method returns verbal feedback for the user which will be displayed in the entry
                answer = append_lock_list.append_locklist(read_locked_list)
                self.e.delete(0, END)
                self.e.insert(0, answer)

        except FileNotFoundError:
            new_lock_list = LockList(self.locked_file_location, self.current_file_location)

            # write_new_file method of lock_list returns answer that a new file was written.
            answer = new_lock_list.write_new_file()
            self.e.delete(0, END)
            self.e.insert(0, answer)

    def delete_current_file(self, MenuGui):
        """Delete the current file if it's not in the locked_list

        Firstly, this method attempts to open the the locked_list.csv. This is necessary to check if the file that
        is to be deleted, is actually allowed to be deleted. If so, deletion proceeds.

        """
        try:
            with open(self.locked_file_location, 'r', newline='') as r:
                reader = csv.reader(r)
                read_locked_list = list(reader)
                to_check = [self.current_file_location]
                if to_check not in read_locked_list:
                    os.remove(str(self.current_file_location))
                    self.e.delete(0, END)
                    self.e.insert(0, "File has been deleted.")
                    MenuGui.list_of_deleted(self.master, self.col_number, self.file_size_int)
                elif to_check in read_locked_list:
                    self.e.delete(0, END)
                    self.e.insert(0, "File can't be deleted.")
        except FileNotFoundError:
            print("no lock_list.csv present.")

    def preview(self):
        """Display preview of image, csv, or text file

        This method first tries to open self.current_file_location as
        a txt/csv file. If the file is something else, A UnicodeError will appear.
        In that case it will try to open the path as an image. If that still does not work,
        it gives up and moves on.

        """

        # try to open and read it as a csv or text file
        try:
            open_file = open(self.current_file_location, 'r')
            read_open_file_again = open_file.readlines(1200)
            Label(self.popup,
                  text=read_open_file_again, wraplength=250
                  ).pack(side=TOP, expand=True, fill=BOTH)

        except FileNotFoundError:
            self.e.delete(0, END)
            self.e.insert(0, "No file here.")

        # Try to open it as an image
        except UnicodeDecodeError:
            try:
                im = Image.open(self.current_file_location)
                pil_im = ImageTk.PhotoImage(im)
                img = Label(self.popup, image=pil_im)
                img.image = pil_im
                img.pack()

            # If it can't open as an image, inform the user that no preview will be given
            except UnidentifiedImageError:
                self.e.delete(0, END)
                self.e.insert(0, "This file is not compatible")

    def rename_file(self):
        """Rename the current file"""

        def apply_new_name(entry, ending):
            """"Using user entry to change filename

            Firstly, it's checked if the user actually entered something. Secondly, it's checked whether the user has
            entered any illegal characters in the file name. thirdly, retrieve all file names excluding their format ex-
            tensions. Create a new list (list_no_end) of all filenames, excluding file extensions, to check if any of them
            match with the user-entered new file name. Lastly, proceed to rename file.

            """

            # Check if user entered anything
            if entry == "":
                self.e.delete(0, END)
                self.e.insert(0, "You entered nothing.")
            else:

                # check if there is a disallowed character present in the user-entered name
                list_of_disallowed_chars = ["\\", "/", "?", "%", "*", ":", "\"", "<", ">", ".", " "]
                if any(i in entry for i in list_of_disallowed_chars):
                    self.e.delete(0, END)
                    self.e.insert(0, "Please don't use {} try to type something again.".format(str(list_of_disallowed_chars)))
                else:

                    # create a list of all file names in current directory excluding their file extensions
                    arr = os.listdir(self.current_directory_path)
                    list_no_end = ['.git', '.idea']
                    for i in arr:
                        list_no_end.append(i.rsplit(sep, 1)[0])

                    # check if there are any matches
                    if entry in list_no_end:
                        self.e.delete(0, END)
                        self.e.insert(0, "Already a file or folder with the same name!")
                    else:

                        # proceed with renaming the file using the entry from the user and the ending we stored before
                        entry_and_format = entry + "." + ending
                        new_name = os.path.join(self.current_directory_path, entry_and_format)
                        try:
                            os.rename(self.current_file_location, new_name)
                            self.popup.destroy()

                        except FileNotFoundError:
                            self.e.delete(0, END)
                            self.e.insert(0, "No file here.")

        # separating name from the format extension (ending), which will be used later.
        sep = '.'
        ending = str(self.current_file_location).rsplit(sep, 1)[1]

        # instructions for the user
        self.e.delete(0, END)
        self.e.insert(0, "Please enter new name below")
        self.e_two.delete(0, END)

        # Button pops up to permanently change the file name change
        Button(
            self.popup, text="PRESS HERE TO RENAME", bg='red', command=lambda: apply_new_name(self.e_two.get(), ending)
        ).pack(side=TOP, expand=True, fill=BOTH)

    def return_to_main(self):
        self.popup.destroy()

from tkinter import *
import os
from AC_Manip_File import FileManipulation


class DirectoryManipulation(Frame):
    """Dealing with subdirectories using the DirectoryManipulation class

    This class is designed to deal with subdirectories within the main menu (MenuGui). It is set up in a similar way,
    It creates buttons for files and directories and will redirect the user to the appropriate location when clicked.
    This class is reused whenever the use wants to access a subdirectory within this directory.

    """
    def __init__(self, master=None, col_number=None, location=None, locked_file_location=0):
        """Variables are initialized and navigational buttons are created.

        :param master: The root from main.
        :param col_number: The name of this directory.
        :param location: Full file path of this directory.
        :param locked_file_location: Location of the csv with un-deletable files

        """
        Frame.__init__(self, master=master)
        self.master = master
        # initialization.
        self.col_number = col_number
        self.location = location
        print("This is a test{}".format(self.location))
        self.locked_file_location = locked_file_location

        # creating the popup window.
        self.popup = Toplevel(master)
        self.popup.title(str(col_number))
        self.popup.grab_set()

        # Label and buttons for dirs
        Label(
            self.popup, text='Directories', background='blue', fg='white'
            ).pack(side=TOP, expand=True, fill=BOTH)
        self.create_buttons_dirs()

        # label and buttons for files
        Label(
            self.popup, text='Files', background='green', fg='white'
            ).pack(side=TOP, expand=True, fill=BOTH)
        self.create_buttons_files()

        # Exit window
        Button(
            self.popup, text="Return", command=lambda: self.popup.destroy()
            ).pack(side=TOP, expand=True, fill=BOTH)

    def create_buttons_dirs(self):
        """Create Buttons for directories within current directory

        Create buttons for all directories within current directory. The corresponding commands launch the use_dir method.

        """
        dirs = next(os.walk(str(self.location)))[1]
        for d in dirs:
            Button(
                self.popup, text=d, command=lambda col_number=d: self.use_dir(col_number)
                ).pack(side=TOP, expand=True, fill=BOTH)

    def create_buttons_files(self):
        """Create Buttons for files

        Create buttons for files within current directory. The corresponding commands will initiate the use_file method.

        """
        files = next(os.walk(str(self.location)))[2]
        for f in files:
            Button(
                self.popup, text=f, command=lambda col_number=f: self.use_file(col_number)
                ).pack(side=TOP, expand=True, fill=BOTH)

    def use_dir(self, col_number_dir):
        """ Initiate DirectoryManipulation class (itself)

        This method initiates a new instance using itself as a class but with different parameters.
        Location_dir is equivalent to the path of the sub directory within this directory.

        """
        location_dir = os.path.join(self.location, col_number_dir)
        DirectoryManipulation(self.master, col_number_dir, location_dir, self.locked_file_location)

    def use_file(self, col_number_file):
        """Initiate the FileManipulation class

        location_file joins the file name that was selected using the button (col_number_file) and its own path (self.
        location) to create the new path with which the FileManipulation class will create a new instance.

        """
        try:
            location_file = os.path.join(self.location, col_number_file)
            FileManipulation(self.master, col_number_file, location_file, self.location, self.locked_file_location)
        except FileNotFoundError:
            print("File has been deleted already!")

from tkinter import *
import os
from AC_Manip_File import FileManipulation
from AB_Manip_SubDir import DirectoryManipulation


class MenuGui(Frame):
    """The main menu as a starting point for any actions

    This is the main menu. It displays all of the directories and files within the current directory.
    The current directory is the directory in which this .py file runs. From now on, this directory will be referred to
    as the so-called 'original directory' because any subsequent navigation through files and subdirectories stem from
    here.

    """

    def __init__(self, master=None, imported_path=None):
        """Initializing window and variables

        Firstly, the window is set up using the frame / root. Secondly, a listbox is created for displaying information
        about things done during the session. Thirdly, methods for creating buttons (accompanied by labels) are called.
        Lastly, these button methods create buttons for all files and directories available.

        :param master: Use the root for a Tkinter
        :param imported_path: The path to the folder in which this program runs

        """

        # initialize root window
        Frame.__init__(self, master=master)
        self.master = master
        self.master.title("Michiel Text Program")
        self.pack(fill=BOTH, expand=1)
        self.current_directory_path = imported_path

        # create a variable that represents the path to the csv that tracks 'un-deletable' files
        name_locked_file = "locked_files.csv"
        self.locked_file_location = os.path.join(str(self.current_directory_path), name_locked_file)
        print(self.locked_file_location)

        # Refresh button
        Button(
            self, text="REFRESH SESSION", command=lambda: self.refresh_button()
        ).pack(side=TOP, expand=True, fill=BOTH)

        # create buttons for subdirectories and files
        self.create_buttons_dirs()
        self.create_buttons_files()

        # Title of the calculated of bytes deleted display
        Label(
            self, text="number of bytes deleted in this session", background='red', fg='white'
        ).pack(side=TOP, expand=True, fill=BOTH)

        # Entry box that keeps track of how many bytes have been deleted during the session
        self.entry_box = Entry(self)
        self.entry_box.pack(side=TOP, expand=True, fill=BOTH)

        # label for the deleted items section
        Label(
            self, text="deleted items in the session.", background='red', fg='white'
        ).pack(side=TOP, expand=True, fill=BOTH)

        # setting up the scrollbar for and a listbox where deleted files will be listed
        sb = Scrollbar(self)
        sb.pack(side=RIGHT, fill=Y)
        self.mylist = Listbox(self, yscrollcommand=sb.set)
        self.mylist.pack(side=TOP, expand=True, fill=BOTH)
        sb.config(command=self.mylist.yview)

    def create_buttons_dirs(self):
        """Create Buttons for directories within current directory

        Create buttons for directories within current directory. The corresponding commands launch the use_dir method.
        One parameter is involved:

            (1) col_number {str} --- Name of the directory to be used

        """
        dirs = next(os.walk(self.current_directory_path))[1]
        Label(
            self, text='Directories', background='blue', fg='white'
        ).pack(side=TOP, expand=True, fill=BOTH)
        for d in dirs:
            Button(
                self, text=d, command=lambda col_number=d: self.use_dir(col_number)
            ).pack(side=TOP, expand=True, fill=BOTH)

    def create_buttons_files(self):
        """Create Buttons for files

        Create buttons for files within current directory. The corresponding commands will initiate the use_file method.
        One parameter is involved in launching this method:

            (1) col_number {str} --- Name of the file to be used

        """
        files = next(os.walk(self.current_directory_path))[2]
        Label(
            self, text='Files', background='green', fg='white'
        ).pack(side=TOP, expand=True, fill=BOTH)
        for f in files:
            Button(
                self, text=f, command=lambda col_number=f: self.use_file(col_number)
            ).pack(side=TOP, expand=True, fill=BOTH)

    def use_dir(self, col_number_dir):
        """ Call DirectoryManipulation class

        This method deals with subdirectories by creating an instance of the dedicated DirectoryManipulation class based
        on the button selected by the user. The following parameters are involved:

            (1) col_number_dir {str} --- The name of the selected directory;
            (2) Location_dir {str} --- The full file path of the dir for which the button was pressed;
            (3) self.locked_file_location {str} --- The location of the un-deletable file csv in the 'original' directory.

        """
        location_dir = os.path.join(self.current_directory_path, col_number_dir)
        DirectoryManipulation(self, col_number_dir, location_dir, self.locked_file_location)

    def use_file(self, col_number_file):
        """ Call FileManipulation class

        This method deals with which ever file is select by the user. It creates an instance of the FileManipulation
        class for the selected file. The following parameters are involved:

            (1) col_number_file {str} = The name of the selected file;
            (2) location_file {str} = The full path of the file for which the button was pressed;
            (3) self.current_directory_path {str} = The path to directory in which the file is located.
            (4) self.locked_file_location {str} = The location of the un-deletable file csv in the 'original' directory.

        """
        try:
            location_file = os.path.join(self.current_directory_path, col_number_file)
            FileManipulation(self, col_number_file, location_file, self.current_directory_path,
                             self.locked_file_location)
        except FileNotFoundError:
            print("File can't be found.")

    def refresh_button(self):
        """ Destroy window and initialize new instance

        When many files are deleted, the main menu still displays them, unless the user refreshes the session.

        """
        self.destroy()
        self.__init__(self.master, self.current_directory_path)

    def list_of_deleted(self, message, file_size):
        """ Listing name and file size of deleted items during the session.

        This method is called from the file manipulation module whenever something is deleted to keep track of it.

        :param message: This variable represents the name of the deleted file
        :param file_size: This variable represents file size
        :return: This method does not return anything.

        """

        # grab whatever is already at the entry
        old_bytes = self.entry_box.get()

        # calculate the new total number of bytes deleted
        try:
            new_bytes = int(old_bytes) + int(file_size)
        except ValueError:
            new_bytes = int(file_size)

        # new total amount of bytes deleted will be inserted in entry.
        self.entry_box.delete(0, END)
        self.entry_box.insert(0, "{} bytes".format(str(new_bytes)))

        # Label for user with deletion information.
        improved_message = "File: {0} \n" \
                           "size: {1} bytes".format(message, file_size)

        self.mylist.insert(END, improved_message)


if __name__ == '__main__':
    CURRENT_DIRECTORY_PATH = os.path.abspath(os.getcwd())
    ROOT = Tk()
    main_menu = MenuGui(ROOT, CURRENT_DIRECTORY_PATH)
    ROOT.mainloop()

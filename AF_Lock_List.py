import csv


class LockList:
    """ Managing un-deletable files

    This class can do two things. Either append an existing list with the file that was selected to be un-deletable, or
    if the locked_list.csv does not exist yet, create it first and then add the file that was selected to be un-deletable.

    """
    def __init__(self, locked_loc, add_file):
        """Initialization

        :param locked_loc: The path of the locked_list.csv file that stores the un-deletable file paths.
        :param add_file: The path of the file that was selected to be un-deletable.

        """

        self.locked_loc = locked_loc
        self.add_file = [add_file]

    def append_locklist(self, read_locked_list):
        """Appending an imported csv file

        :param read_locked_list: The contents of locked_file.csv in list-form.
        :return: return a message to be displayed from the AD_manip_file_one class.

        """

        with open(self.locked_loc, 'a+', newline='') as f:
            writer = csv.writer(f)
            if self.add_file in read_locked_list:
                return "Already in list."
            else:
                writer.writerow(self.add_file)
                return "Successfully locked file."

    def write_new_file(self):
        """Creating new csv file and writing the self.add_file to it.

        :return: return a message for the user to know what has happened.

        """

        with open(self.locked_loc, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.add_file)
            return "A new csv file was created."

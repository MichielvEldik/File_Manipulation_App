from Crypto.Cipher import AES


class Encryption:
    """Encryption of a given text or csv file

    The class creates encrypted versions of files. A certain key is used for this (self.key). This same key will be used
    for all files. This is not the most secure way. It could be possible to generate a random key for every file and
    return it to the user in the entry window or a doc file. That would be more secure. If I had time, I would implement
    this functionality.

    """
    def __init__(self, file_location, current_directory, col_number, plain_text_file):
        """Initializing the variables

        :param file_location: Full file path of current file
        :param current_directory: Directory path of file in use
        :param col_number: File name (including format extension)
        :param plain_text_file: The actual content of the file that has already been read outside of the class.

        """

        # initializing variables
        self.file_location = file_location
        self.current_directory = current_directory
        self.cole_number = col_number
        self.plain_text_file = plain_text_file

        # setting up cipher using randomly generated binary key
        self.key = b'\xc3\xb9\x1bs\x15=\xe71\x03\xb8\x94\xda\x93e\xf5N'
        cipher = AES.new(self.key)
        self.encryption(self.plain_text_file, cipher)

    def encryption(self, plain_text_file, cipher):
        """Encryption turns text file into binary file

        :param plain_text_file: The str version of the opened txt file.
        :param cipher: the cipher used for encryption, which was created with the unique key
        :return: the method is not fruitful and does not return anything.

        """
        def pad(s):
            """ Quick abstraction for padding."""
            return s + ((16 - len(s) % 16) * '{')

        # actual encryption using padding and encryption algorithm
        encrypted = cipher.encrypt(pad(plain_text_file))
        self.write_file(encrypted)

    def write_file(self, encrypted):
        """Write the encrypted message to a new file.

        this method splits a file name on the basis of the last period of that file name.
        E.g. the file: Michiel.van.Eldik.txt will be split so that 'Michiel.van.Eldik' will be seperated from
        'txt'. This helps in naming the encrypted version of the file.

        """

        # Creating new name
        sep = '.'
        rest = self.file_location.rsplit(sep, 1)[0]
        ending = self.file_location.rsplit(sep, 1)[1]
        new_name = "{0}(ENCRYPTED){1}{2}".format(rest, sep, ending)

        # use new name to write new file
        with open(new_name, 'bw') as f:
            f.write(encrypted)

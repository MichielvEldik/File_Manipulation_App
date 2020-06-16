from Crypto.Cipher import AES


class Decryption:
    """Decryption of encrypted binary files.

    This takes the same key and padding config to decrypt the encrypted message.

    """

    def __init__(self, file_location, current_directory, col_number, binary_file):
        """ Initializing variables

        :param file_location: Full path of the current file
        :param current_directory: Full path of the current directory
        :param col_number: name (including format extension) of current file
        :param binary_file: the actual content of the file that has already been read outside of this class.

        """
        self.file_location = file_location
        self.current_directory = current_directory
        self.cole_number = col_number
        self.binary_file = binary_file

        # ask for the key...
        self.key = b'\xc3\xb9\x1bs\x15=\xe71\x03\xb8\x94\xda\x93e\xf5N'
        cipher = AES.new(self.key)

        self.decryption(self.binary_file, cipher)

    def decryption(self, binary_file, cipher):
        """ Decryption

        :param binary_file: The actual file that has beenm
        :param cipher: The cipher created with use of the key
        :return: The method doesn't return anything.
        """
        # decoding / decrypting
        dec = cipher.decrypt(binary_file).decode('utf-8')
        pad = dec.count('{')
        decrypted_message = dec[:len(dec)-pad]
        print(dec[:len(dec)-pad])

        # Creating a new name
        sep = '.'
        before_last_period = self.file_location.rsplit(sep, 1)[0]
        after_last_period = self.file_location.rsplit(sep, 1)[1]
        new_name = "{0}(DECRYPTED){1}{2}".format(before_last_period, sep, after_last_period)

        # writing a new file
        with open(new_name, 'w') as d:
            d.write(decrypted_message)

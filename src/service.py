import datetime
import os
from base64 import b64encode, b64decode

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from json import dump, load
import hashlib

from src.sets import SERVICES


class Service:

    def __init__(self, master, service_name):

        self.master = master
        self.service_name = service_name

    def __str__(self):
        return self.service_name

    def save(self, login, password):

        self.login = login
        self.password = password
        self.cipher = self.__encrypt(self.master)

        encrypted_passwd = {"hash": self.cipher}
        encrypted_passwd.update({"login": self.login, "time": str(datetime.datetime.now().date())})

        with open(os.path.join(SERVICES, self.service_name), 'w') as file:
            dump(encrypted_passwd, file, indent=4, ensure_ascii=False)

    def get(self):
        with open(os.path.join(SERVICES, self.service_name), 'r') as file:
            return load(file)["login"], self.__decrypt(self.master)

    def remove(self):
        os.remove(os.path.join(SERVICES, self.service_name))

    def change_master(self, master):
        self.master = master
        login, password = self.get()
        self.remove()
        self.save(login, password)

    def __encrypt(self, master) -> str:
        salt = get_random_bytes(AES.block_size)

        private_key = hashlib.scrypt(
            master.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

        cipher_config = AES.new(private_key, AES.MODE_GCM)

        cipher_text, tag = cipher_config.encrypt_and_digest(self.password.encode('utf-8'))

        return f"{b64encode(salt).decode('utf-8')}" \
               f"{b64encode(cipher_config.nonce).decode('utf-8')}" \
               f"{b64encode(tag).decode('utf-8')}" \
               f"{b64encode(cipher_text).decode('utf-8')}"

    def get_hash(self):
        with open(os.path.join(SERVICES, self.service_name), 'r') as file:
            return load(file)["hash"]

    def __parse_hash(self, block_size=24) -> tuple:

        cipher = self.get_hash()
        return tuple(map(b64decode, (cipher[:block_size], cipher[block_size:block_size * 2],
                                     cipher[block_size * 2:block_size * 3], cipher[block_size * 3:])))

    def __decrypt(self, master) -> str:
        """

        :param master:
        :return:
        """
        salt, nonce, tag, cipher_text = self.__parse_hash()
        # generate the private key from the password and salt
        private_key = hashlib.scrypt(
            master.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

        # create the cipher config
        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

        # decrypt the cipher text
        try:
            return cipher.decrypt_and_verify(cipher_text, tag).decode('utf-8')
        except ValueError:
            return ""

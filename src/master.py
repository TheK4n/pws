
import os
from src.service import Service
import hashlib

from src.sets import *


class Master:

    SALT_LENGTH = 128  # move to settings
    HASH_METHOD = 'sha512'
    HASH_COUNT = 100000

    def __init__(self, password):
        self.password = password
        self.encoded_password = self.__encode_master_password(password)

    def __encode_master_password(self, passwd):
        salt = os.urandom(self.SALT_LENGTH)
        return salt + hashlib.pbkdf2_hmac(self.HASH_METHOD, passwd.encode('utf-8'), salt, self.HASH_COUNT)

    @staticmethod
    def change_master_in_services(old_master, new_master):
        for s in os.listdir(SERVICES):
            service = Service(old_master, s)
            l, p = service.get()
            service.remove()
            service = Service(new_master, s)
            service.save(l, p)

    def write(self, password):
        with open(SHADOW, 'wb') as file:
            self.password = password
            self.encoded_password = self.__encode_master_password(password)
            file.write(self.encoded_password)

    @staticmethod
    def __get_master_hash():
        with open(SHADOW, 'rb') as file:
            return file.read()

    @property
    def hash(self):
        return self.__get_master_hash()

    def check(self) -> bool:
        master_hash = self.hash
        salt_from_storage = master_hash[:self.SALT_LENGTH]
        key_from_storage = master_hash[self.SALT_LENGTH:]
        key = hashlib.pbkdf2_hmac(self.HASH_METHOD, self.password.encode('utf-8'), salt_from_storage, self.HASH_COUNT)
        return key == key_from_storage

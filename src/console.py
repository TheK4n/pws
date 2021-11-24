import datetime
import os
from getpass import getpass
from json import dump, load

from src.master import Master
from src.service import Service
from src.sets import *

FORBIDDEN_SYMBOLS = r'\|/:,*?"<>+.%!@'

help_title = r"""
add "service"
get "service"
rm "service"

set "setting"

quit
exit
q
"""


class Console:

    prompt = '\npws > '

    def __init__(self, master_passwd):
        self.hst_file = open(HISTORY, 'a')
        self.master = Master(master_passwd)

        if not os.path.exists(SHADOW):
            self.master.write("root")

        if not os.path.exists(SETTINGS):
            with open(SETTINGS, 'w') as file:
                dump({"chtime": 60}, file, indent=4, ensure_ascii=False)

        if not os.path.exists(HISTORY):
            with open(HISTORY, 'w'):
                pass

        if not os.path.exists(SERVICES):
            os.mkdir(SERVICES)

    def __add(self, service_name: str):

        login = input("[?] login: ")
        passwd = getpass("[?] Enter password: ")
        passwd_rep = getpass("[?] Repeat password: ")
        if passwd_rep == passwd:
            service = Service(self.master.password, service_name)
            service.save(login, passwd)
            print(f"[+] Added {service_name}")
        else:
            print('[X] Passwords did not match')

    def __get(self, service_name):

        service = Service(self.master.password, service_name)
        try:
            l, p = service.get()
        except FileNotFoundError:
            print(f"[X] Service \"{service_name}\" not found")
        else:
            answer = input("[?] Show password? Y/n ")
            if answer in ['Y', 'y']:
                print(f"\n[*] Service \"{service_name}\":\n\tLogin: {l}\n\tPassword: {p}")
            else:
                # print(f"\n[*] Service \"{service_name}\":\n\tLogin: {l}\n\tPassword: *copied to clipboard*")
                # pyperclip.copy(p)
                pass

    def __rm(self, service_name):
        service = Service(self.master.password, service_name)
        try:
            service.remove()
            print(f"[-] Service \"{service_name}\" removed")
        except FileNotFoundError:
            print(f"[X] Service \"{service_name}\" not found")

    def __set(self, setting: str):
        match setting:
            case "master", sub:
                new_master = getpass("[?] Enter new master password: ")
                if new_master == getpass("[?] Repeat new master password: "):
                    match sub:
                        case "*":
                            self.master.change_master_in_services(self.master.password, new_master)
                            self.master.write(new_master)
                            print("[+] Setting master changed")
                        case service_name:
                            service = Service(self.master.password, service_name)
                            try:
                                service.change_master(new_master)
                                print("[+] Service master changed")
                            except FileNotFoundError:
                                print(f"[X] Service \"{service_name}\" not found")
            case _:
                print(f"\n[X] Unknown setting")

    def loop(self):
        while True:
            command = input(self.prompt)
            self.hst_file.write(command + '\n')
            match command.split():
                case "add", service_name:
                    wrong_name = False
                    for sym in service_name:
                        if sym in FORBIDDEN_SYMBOLS:
                            print(f"[X] Wrong char in service name: \"{sym}\"")
                            wrong_name = True
                            break

                    if wrong_name:
                        continue
                    self.__add(service_name)

                case "get", service_name:
                    self.__get(service_name)

                case "set", *setting:
                    self.__set(setting)

                case "rm", service_name:
                    self.__rm(service_name)

                case ["ls"]:
                    for i in os.listdir(SERVICES):
                        print(i)

                case ['c'] | ['clear']:
                    os.system(["cls", "clear"][os.name == 'posix'])

                case ["q"] | ["exit"] | ["quit"]:
                    print('\n[X] PWS stopped')
                    exit(1)

                case ["help"]:
                    print(help_title)

                case _:
                    print(f"\n[X] Unknown command")

    @staticmethod
    def get_expired_passwords():
        res = []

        chtime = int(load(open(SETTINGS, 'r'))["chtime"])

        for s in os.listdir(SERVICES):
            if datetime.datetime.now() - datetime.datetime.strptime(load(open(os.path.join(SERVICES, s), 'r'))["time"],
                                                                    '%Y-%m-%d') \
                    > datetime.timedelta(chtime):
                res.append(s)
        if res:
            print("[*] Expired:")
            c = 0
            for i in res:
                if c >= 3:
                    print(i)
                    c = 0
                else:
                    print(i, end="\t")
                    c += 1

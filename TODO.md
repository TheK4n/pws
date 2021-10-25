1. Console Passwords Storage

   * Master password - PBKDF2 
   * Passwords and settings - AES

```text
master password (PBKDF2 + pepper(custom) + username) to get access
```


```text
./pws  # -> enter mpasswd -> PWS terminal
lst  # list services

add "service"  # -> enter login -> enter passwd
get "service"  # -> enter master password -> Y/n -> Show in console or copy to clipboard

set master  # -> get_passwd() -> repeat mpasswd  # change master password
set qtime "360"  # quit from terminal time in seconds
set chtime "365"  # time to change passwords in days
set slevel "1-3"  # power level

quit|q|exit  # exit from PWS

rnd "level"  # get random passwd
pws -r "level"  # get random passwd without console
```

```text
.pws_history
[*] asdasd
[+] changed
[!] warn
[-] asd
5min quit from PWS terminal and clear
list of same passwords
list of weak passwords
notify to change passwords
```

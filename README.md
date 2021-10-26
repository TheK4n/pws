<h1 align="center">Password Storage</h1>

<p align="center">
  <a href="https://github.com/TheK4n">
    <img src="https://img.shields.io/github/followers/TheK4n?label=Follow&style=social">
  </a>
  <a href="https://github.com/TheK4n/pws">
    <img src="https://img.shields.io/github/stars/TheK4n/pws?style=social">
  </a>
</p>


* [Project description](#chapter-0)
* [Installation](#chapter-1)
* [Usage](#chapter-2)


<a id="chapter-0"></a>
## Project description 

Secure passwords storage on python\
Master password hashing SHA512\
Passwords encrypt with AES



<a id="chapter-1"></a>
## Installation:

Clone repository and installing dependencies:

```bash
git clone https://github.com/TheK4n/pws.git
cd pws
python3.10 -m pip install -r requirements.txt
chmod u+x pws
ln -s $PWD/pws ~/bin/pws
```


<a id="chapter-2"></a>
## Usage

```./pws``` - Enter in pws terminal

* Enter password "root"
* ```set master``` -> Enter old password "root" -> Enter and repeat new master password
* ```add "service"``` -> Enter master password -> Enter new service login -> Enter and repeat new service password
* ```ls``` Shows existing services
* ```get "service"``` Shows login and password of service
* ```rm "service"``` Removes service



<h1 align="center"><a href="#top">▲</a></h1>

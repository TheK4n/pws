SC=pws
iPATH=~/bin

all: install

install:
	python3.10 -m pip install -r requirements.txt
	chmod u+x $(SC)
	ln -s $(PWD)/$(SC) $(iPATH)/$(SC)

uninstall:
	rm $(iPATH)/$(SC)

clean:
	rm -rf .gitignore README.md .git LICENSE
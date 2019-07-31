all: get unzip process

get:
	wget --input-file urls.txt --directory-prefix data --no-clobber

unzip:
	unzip 'data/*.zip' -d data

process:
	python3 process.py

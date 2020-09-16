all:
	pipenv update
	pipenv run pyinstaller src/rvpkg.py --onefile

install:
	install -v -m 755 dist/rvpkg /usr/bin/rvpkg

clean:
	pipenv --rm
	rm -rf build/ dist/
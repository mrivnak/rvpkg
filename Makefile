all:
	pipenv update --three
	pipenv run pyinstaller src/rvpkg.py --onefile

clean:
	pipenv -rm
	rm -rf build/ dist/
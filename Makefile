all:
	pipenv update
	pipenv run pyinstaller src/rvpkg.py --onefile

install:
	install -v -d -m 644 /usr/share/rvpkg
	install -v -d -m 644 /var/lib/rvpkg
	install -v -m 755 fs/etc/rvpkg.yaml /etc/rvpkg.yaml
	install -v -m 755 fs/usr/share/rvpkg/packages.yaml /usr/share/rvpkg/packages.yaml
	touch /var/lib/rvpkg/packages.log
	chmod 755 /var/lib/rvpkg/packages.log
	install -v -m 755 dist/rvpkg /usr/bin/rvpkg

clean:
	pipenv --rm
	rm -rf build/ dist/

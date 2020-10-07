all:
	python3 -m virtualenv venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pyinstaller src/rvpkg.py --onefile

install:
	install -v -d -m 755 /usr/share/rvpkg
	install -v -d -m 755 /var/lib/rvpkg
	install -v -m 644 fs/etc/rvpkg.yaml /etc/rvpkg.yaml
	install -v -m 644 fs/usr/share/rvpkg/packages.yaml /usr/share/rvpkg/packages.yaml
	touch /var/lib/rvpkg/packages.log
	chmod 644 /var/lib/rvpkg/packages.log
	install -v -m 755 dist/rvpkg /usr/bin/rvpkg

clean:
	rm -rf build/ dist/ venv/

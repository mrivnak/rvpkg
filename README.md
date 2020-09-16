# rvpkg

RiVnak Package Manager. Small package organization system for use with my [B]LFS system.

## Requirements

(Required for build only)

- python 3.6+
- pipenv

## Installation

```shell
make
sudo make install
```

### Cleaning up

Since pipenv leaves files on the system outside of the build directory it is highly recommended to clean up those files

```shell
make clean
```

Purpose
=======

This project contains **podload**, a simple Python utility to download podcasts.

Install
=======

Install the package from our PyPi server:

```
pip3 install -i https://pypi.confirm.ch podload
```

Install the package from source:

```
pip3 install confirm-utils@git+https://git.confirm.ch/confirm/podload.git
```

Usage
=====

The usage of ``podload`` is quite simple:

```
usage: podload [-h] [-a AGE] [-d] [-v] directory [url]

The simple podcast loader.

positional arguments:
  directory          the name of the podcasts directory
  url                a podcast URL to add

optional arguments:
  -h, --help         show this help message and exit
  -a AGE, --age AGE  the max age
  -d, --debug        enable debug mode
  -v, --verify       verify the file size as well
```

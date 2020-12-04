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
usage: podload [-h] [-d] directory {info,add,download} ...

The simple podcast loader.

positional arguments:
  directory            the name of the podcasts directory
  {info,add,download}
    info               display the podcast infos
    add                add a new podcast
    download           download the latest episodes

optional arguments:
  -h, --help           show this help message and exit
  -d, --debug          enable debug mode
```

For example, to add the "TED Talks Daily" Podcast to `/Volumes/XTRAINERZ` you can run this:

```
podload /Volumes/XTRAINERZ add http://feeds.feedburner.com/TEDTalks_audio 
```

From now on you can download the latest episodes by executing:

```
podload /Volumes/XTRAINERZ download
```

If you want more episodes than just the last 7 days, you can specify the `-a` argument:

```
podload /Volumes/XTRAINERZ download -a 20
```

Podload will remember it and will automatically use the same age in the future, as long as you don't specify `-a`.

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
usage: podload [-h] [-d] [-r RETENTION] directory {info,clean,add,download} ...

The simple podcast loader.

positional arguments:
  directory                            the name of the podcasts directory
  {info,clean,add,download}
    info                               display the podcast infos
    clean                              clean old episodes
    add                                add a new podcast
    download                           download the latest episodes

optional arguments:
  -h, --help                           show this help message and exit
  -d, --debug                          enable debug mode
  -r RETENTION, --retention RETENTION  an alternative retention in days
```

For example, to add the "Wired UK" Podcast to `/Volumes/XTRAINERZ` you can run this:

```bash
podload /Volumes/XTRAINERZ add https://www.wired.co.uk/rss/podcast/wired-podcast
```

*The podcast is added to a sub directory, together with a metadata file which holds all the 
important bits for the podload manager.*

From now on you can **download the latest episodes** by executing:

```bash
podload /Volumes/XTRAINERZ download
```

To **clean up old episodes**, run this:

```bash
podload /Volumes/XTRAINERZ clean
```

To display all the infos run this:

```
podload /Volumes/XTRAINERZ info

The WIRED Podcast (14 days retention):
    2020-11-20 16:04.mp3  How China crushed Covid-19
    2020-11-27 12:12.mp3  How to make sure Christmas isn't a Covid-19 disaster
    2020-12-04 12:00.mp3  What the Covid-19 vaccines mean for returning to work
```

By default a **retention time of 7 days** is used.
However, you can either override that when `add`ing the podcast (permanent) or when `download`ing podcasts (temporarily) by using the `-r` argument.

```bash
# Permanent:
podload /Volumes/XTRAINERZ -r 14 add https://www.wired.co.uk/rss/podcast/wired-podcast

# Temporarily:
podload /Volumes/XTRAINERZ -r 14 download
```

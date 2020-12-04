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
usage: podload [-h] [-d] directory {info,clean,add,download,set-retention} ...

The simple podcast loader.

positional arguments:
  directory                             the name of the podcasts directory
  {info,clean,add,download,set-retention}
    info                                display the podcast infos
    clean                               clean old episodes
    add                                 add a new podcast
    download                            download the latest episodes
    set-retention                       set a new retention

optional arguments:
  -h, --help                            show this help message and exit
  -d, --debug                           enable debug mode
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
However, you can set another podcast default when `add`ing the podcast by using the `-r` argument, or by calling `set-retention` afterwards. You can also override the retention temporarily when `clean`ing or `download`ing podcasts by using the `-r` argument.

```bash
# Permanent:
podload /Volumes/XTRAINERZ add -r 14 https://www.wired.co.uk/rss/podcast/wired-podcast
podload /Volumes/XTRAINERZ set-retention "The WIRED Podcast" 14

# Temporarily:
podload /Volumes/XTRAINERZ clean -r 14
podload /Volumes/XTRAINERZ download -r 14
```

Introduction
============

**Podload** is a radically simple Python tool to manage podcasts with no fuzz.
It includes the following features:

- **Add** new podcasts via their URL
- Automatically **download** the latest episodes 
- Automatically **clean** up old episodes
- Defining the **retention** time for each podcast
- Putting podcasts into **subdirectories**, even nested ones

I'm using this tool to always have the latest podcasts on my [Aftershokz Xtrainers](https://aftershokz.com/products/xtrainerz).

Installation
============

Install the package via PyPi:

```
pip3 install podload
```

Install the package from source:

```
pip3 install podload@git+https://git.confirm.ch/confirm/podload.git
```

Usage
=====

The usage of ``podload`` is quite simple:

```
usage: podload [-h] [-d] [-b BASEDIR] {info,clean,add,download,update,set-retention} ...

The simple podcast loader.

positional arguments:
  {info,clean,add,download,update,set-retention}
    info                                display the podcast infos
    clean                               clean old episodes
    add                                 add a new podcast
    download                            download the latest episodes
    update                              shortcut for download, followed by clean
    set-retention                       set a new retention

options:
  -h, --help                            show this help message and exit
  -d, --debug                           enable debug mode
  -b BASEDIR, --basedir BASEDIR         base directory
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

To **download and clean up**, run this:

```bash
podload /Volumes/XTRAINERZ update
```

To display all the infos run this:

```
podload /Volumes/XTRAINERZ info

The WIRED Podcast (14 days retention):
    2021-08-20 14:15 - Afghans are racing to erase their online lives
    2021-08-27 11:00 - Is your name ruining your life?
    2021-08-26 09:00 - Introducing Food People
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

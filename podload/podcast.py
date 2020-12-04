'''
Podcast module.
'''

__all__ = (
    'Podcast',
)

import datetime
import email.utils
import json
import logging
import os
import urllib.request
import urllib.parse

import feedparser
import pytz

#: The logger instance.
LOGGER   = logging.getLogger(__name__)

#: The local timezone to use.
TIMEZONE = pytz.timezone('Europe/Zurich')

#: The default max age.
DEFAULT_AGE = 7


class Podcast:
    '''
    A single podcast.

    :param str podcast_dir: The podcast directory
    '''

    #: The name of the metadata file.
    metadata_filename = '.podload'

    #: Accepted link mime types.
    accepted_types = (
        'audio/mpeg',
    )

    @classmethod
    def create(cls, url, podcasts_dir):
        '''
        Create a new podcast from an URL.

        This will create a new directory with the meta file in it.

        :param str url: The podcast URL
        :param str podcasts_dir: The podcasts directory

        :return: The podcast instance
        :rtype: Podcast
        '''
        LOGGER.info('Creating new podcast from "%s"', url)

        title         = feedparser.parse(url).feed.title
        podcast_dir   = os.path.join(podcasts_dir, title)
        metadata_file = os.path.join(podcast_dir, cls.metadata_filename)

        if not os.path.exists(podcast_dir):
            os.makedirs(podcast_dir)

        if os.path.exists(metadata_file):
            LOGGER.error('Podcast metadata file "%s" is already existing', metadata_file)
        else:
            with open(metadata_file, 'w') as file:
                json.dump({
                    'url': url,
                    'title': title,
                }, file)

        return cls(podcast_dir)

    def __init__(self, podcast_dir):
        '''
        Constructor.
        '''
        LOGGER.debug('Initialising podcast at "%s"', podcast_dir)

        self.podcast_dir      = podcast_dir
        self.metadata_file    = os.path.join(podcast_dir, self.metadata_filename)
        self.metadata         = {}
        self.feed             = []
        self.current_download = None

        self.load_metadata()
        self.clean_metadata()
        self.parse()

    def __str__(self):
        '''
        The informal string representation of the podcast.

        :return: The title
        :rtype: str
        '''
        return self.metadata['title']

    def __repr__(self):
        '''
        The official string representation of the podcast.

        :return: The class w/ title
        :rtype: str
        '''
        return f'<{self.__class__.__name__}: {self.metadata["title"]}>'

    @property
    def info(self):
        '''
        The informations of the podcasts.

        :return: The filename & title
        :rtype: generator
        '''
        for file in os.listdir(self.podcast_dir):
            if not file.startswith('.'):
                yield file, self.metadata.get('episodes', {}).get(file, '')

    def clean_metadata(self):
        '''
        Clean the metadata.
        '''
        if 'episodes' not in self.metadata:
            return

        episodes = self.metadata['episodes']
        delete   = []

        for episode in episodes:
            if not os.path.exists(os.path.join(self.podcast_dir, episode)):
                delete.append(episode)

        for item in delete:
            del episodes[item]

        self.save_metadata()

    def load_metadata(self):
        '''
        Load the metadata from disk.
        '''
        LOGGER.debug('Loading metadata from "%s"', self.metadata_file)

        with open(self.metadata_file, 'r') as file_handle:
            self.metadata = json.load(file_handle)

    def save_metadata(self):
        '''
        Save the metadata to disk.
        '''
        LOGGER.debug('Saving metadata to "%s"', self.metadata_file)

        with open(self.metadata_file, 'w') as file_handle:
            json.dump(self.metadata, file_handle)

    def parse(self):
        '''
        Parse the podcast feed.
        '''
        url = self.metadata['url']

        LOGGER.debug('Parsing podcasts at "%s"', url)

        self.feed = feedparser.parse(url)

        self.metadata['title'] = self.feed.feed.title  # pylint: disable=no-member
        self.save_metadata()

    def download(self, age=None, verify=False):  # pylint: disable=too-many-locals
        '''
        Download all episodes within a certain time range.

        :param age: The maximal age in days
        :type age: None or int
        :param bool verify: Verify the file size and redownload if missmatch
        '''
        if age:
            age = self.metadata['age'] = int(age)
        else:
            age = self.metadata.setdefault('age', DEFAULT_AGE)

        episodes  = self.metadata.setdefault('episodes', {})
        threshold = datetime.datetime.now(tz=TIMEZONE) - datetime.timedelta(days=age)

        for entry in self.feed.entries:  # pylint: disable=no-member
            title     = entry.title
            published = email.utils.parsedate_to_datetime(entry.published)
            links     = [link for link in entry.links if link.type in self.accepted_types]

            if published < threshold:
                LOGGER.debug('Ignoring "%s" because it\'s older than %d days', title, age)
                continue

            if not links:
                LOGGER.debug('Ignoring "%s" because no acceptable link types found', title)
                continue

            link      = links[0].href
            suffix    = os.path.splitext(urllib.parse.urlparse(link).path)[1]
            date_str  = published.strftime('%Y-%m-%d %H:%M')
            file_name = f'{date_str}{suffix}'
            file_path = os.path.join(self.podcast_dir, file_name)
            exists    = os.path.exists(file_path)

            if not verify and exists:
                LOGGER.debug('Ignoring "%s" because it\'s already existing', title)
                continue

            with urllib.request.urlopen(link) as response:
                if exists and int(response.headers['content-length']) == os.stat(file_path).st_size:
                    LOGGER.debug(
                        'Ignoring "%s" because it\'s already existing and filesize matches', title)
                    continue
                if exists:
                    LOGGER.warning('Redownloading "%s" as the file size missmatches', title)
                else:
                    LOGGER.info('Downloading podcast episode "%s" to "%s"', title, file_path)

                with open(file_path, 'wb') as file:
                    file.write(response.read())

                episodes[file_name] = title
                self.save_metadata()

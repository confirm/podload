'''
Podcast manager module.
'''

__all__ = (
    'PodcastManager',
)

import argparse
import logging
import os

from .podcast import Podcast

LOGGER = logging.getLogger(__name__)


class PodcastManager:
    '''
    The podcast manager.

    :param str podcasts_dir: The podcast directory
    '''

    def __init__(self, podcasts_dir):
        '''
        Constructor.
        '''
        self.podcasts_dir = podcasts_dir
        self.podcasts     = []

        self.load_podcasts()

    def load_podcasts(self):
        '''
        Load the podcasts from the disk.
        '''
        LOGGER.info('Loading podcasts from %s', self.podcasts_dir)

        if not os.path.exists(self.podcasts_dir):
            LOGGER.warning('Directory %s is missing, not loading podcasts', self.podcasts_dir)
            return

        for root, dirs, files in os.walk(self.podcasts_dir):  # pylint: disable=unused-variable
            for file in files:
                if file != Podcast.metadata_filename:
                    continue
                self.podcasts.append(Podcast(os.path.join(root)))

    def add_podcast(self, url):
        '''
        Add a new podcast.

        :param str url: The podcast URL
        '''
        self.podcasts.append(Podcast.create(url, self.podcasts_dir))

    def download(self, **kwargs):
        '''
        Download all episodes.

        :param dict kwargs: The kwargs to pass to :meth:`podload.podcast.Podcast.download()`
        '''
        for podcast in self.podcasts:
            podcast.download(**kwargs)


def main():
    '''
    Run the CLI script.
    '''
    parser     = argparse.ArgumentParser(description='The simple podcast loader.')
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')
    parser.add_argument('directory', help='the name of the podcasts directory')

    subparsers = parser.add_subparsers(dest='action', required=True)

    subparsers.add_parser(name='info', help='display the podcast infos')

    add = subparsers.add_parser(name='add', help='add a new podcast')
    add.add_argument('url', nargs='?', help='a podcast URL to add')

    download = subparsers.add_parser(name='download', help='download the latest episodes')
    download.add_argument('-a', '--age', help='the max age')
    download.add_argument('-v', '--verify', action='store_true', help='verify the file size')

    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.DEBUG if args.debug else logging.INFO,
    )

    manager = PodcastManager(args.directory)

    if args.action == 'info':
        for podcast in manager.podcasts:
            print(podcast)
            for file, title in podcast.info:
                print(f'    {file}  {title}')

    elif args.action == 'add':
        manager.add_podcast(args.url)

    elif args.action == 'download':
        manager.download(age=args.age, verify=args.verify)


if __name__ == '__main__':
    main()

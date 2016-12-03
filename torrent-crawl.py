#!/usr/bin/env python2.7

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import sys
import os
import configparser
import json
import argparse

from xanaxapi import XanaxAPI

from _constants import __site_url__


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog='xanaxbetter')
    parser.add_argument('-s', '--snatches', type=int, help='minimum amount of snatches required before transcoding',
                        default=5)
    parser.add_argument('-b', '--better', type=int, help='better transcode search type',
                        default=3)
    parser.add_argument('-c', '--count', type=int, help='backlog max size', default=5)
    parser.add_argument('--config', help='the location of the configuration file',
                        default=os.path.expanduser('~/.xanaxbetter/config'))
    parser.add_argument('--cache', help='the location of the cache',
                        default=os.path.expanduser('~/.xanaxbetter/cache-crawl'))

    args = parser.parse_args()

    config = configparser.SafeConfigParser()
    try:
        open(args.config)
        config.read(args.config)
    except:
        print("please run xanaxbetter once")
        sys.exit(2)

    username = config.get('xanax', 'username')
    password = config.get('xanax', 'password')
    torrent_dir = os.path.expanduser(config.get('xanax', 'torrent_dir'))

    print('Logging in to %s...' % __site_url__)
    api = XanaxAPI(username, password)

    try:
        cache = json.load(open(args.cache))
    except:
        cache = []
        json.dump(cache, open(args.cache, 'wb'))

    while len(cache) < args.count:
        print('Refreshing better.php and finding %i candidates' % (args.count - len(cache)))
        for torrent in api.get_better(args.better):
            if len(cache) >= args.count:
                break

            print("Testing #%i" % torrent['id'])
            info = api.get_torrent_info(torrent['id'])
            if info['snatched'] < args.snatches:
                continue

            print("Fetching #%i with %i snatches" % (torrent['id'], info['snatched']))

            with open(os.path.join(torrent_dir, '%i.torrent' % torrent['id']), 'wb') as f:
                f.write(api.get_torrent(torrent['id']))

            torrent['hash'] = info['infoHash'].upper()
            torrent['done'] = False

            cache = json.load(open(args.cache))
            cache.append(torrent)
            json.dump(cache, open(args.cache, 'wb'))

    print('Nothing left to do')

if __name__ == '__main__':
    main()

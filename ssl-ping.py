#!/usr/bin/env python

import argparse
import requests
import sys
import time
import os


def ping(url, expected_status=200):

    ca_file = os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'cacert.pem')

    try:
        r = requests.get(url, verify=ca_file)
    except Exception as e:
        sys.stderr.write('Error: ' + str(e) + '\n')
        return False
    if r.status_code == expected_status:
        sys.stdout.write('.')
    else:
        sys.stdout.write('*')
    return True


def main(args):

    print('*** Pinging: %s ***' % args.url)

    try:
        while True:
            result = ping(args.url)
            sys.stdout.flush()
            # exit with error if not ignored
            if not args.ignore_errors and not result:
                sys.exit(99)
            time.sleep(1)

    except KeyboardInterrupt:
        sys.stdout.write('\n' + 'Shutting down.' + '\n')
        sys.exit(0)

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SSL Ping')
    parser.add_argument('url', nargs='?', type=str, help='URL of host to ping')
    parser.add_argument('--ignore-errors', action="store_true", default=False, dest="ignore_errors", help='Ignore Errors')

   # Init parser if args passed
    if len(sys.argv) > 1:
        args = parser.parse_args()
        main(args)
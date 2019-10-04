#!/usr/bin/env python3

import sys
import json
import argparse
import singer
from singer import metadata, utils
from tap_darksky.client import DarkskyClient
from tap_darksky.discover import discover
from tap_darksky.sync import sync

LOGGER = singer.get_logger()

REQUIRED_CONFIG_KEYS = [
    'secret_key',
    'language',
    'units',
    'location_list_1',
    'start_date',
    'user_agent'
]

def do_discover():
    LOGGER.info('Starting discover')
    catalog = discover()
    json.dump(catalog.to_dict(), sys.stdout, indent=2)
    LOGGER.info('Finished discover')


@singer.utils.handle_top_exception(LOGGER)
def main():

    parsed_args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    with DarkskyClient(parsed_args.config['secret_key'],
                       parsed_args.config['user_agent']) as client:

        state = {}
        if parsed_args.state:
            state = parsed_args.state

        if parsed_args.discover:
            do_discover()
        elif parsed_args.catalog:
            sync(client=client,
                 config=parsed_args.config,
                 catalog=parsed_args.catalog,
                 state=state)

if __name__ == '__main__':
    main()

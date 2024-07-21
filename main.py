# -*- coding: utf-8 -*-
"""Main script for folder synchronization."""

import argparse
import logging
import os
import shutil
from datetime import timedelta

import timeloop

from logger import Logger

logger = logging.getLogger('sync_log.log')


def add_parser():
    """Parsing arguments"""
    parser = argparse.ArgumentParser(description='Synchronizing folders')
    parser.add_argument("source_folder_path", help="Path to source folder")
    parser.add_argument("replica_folder_path", help="Path to replica folder")
    parser.add_argument("sync_interval", help="Time between each sync operation", nargs='?', default=1)
    parser.add_argument("log_path", help="Path to log output")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    script_args = add_parser()
    tl = timeloop.Timeloop()

    logger = Logger(f'{script_args.log_path}\\sync_log.log', level='debug')

    source_dir = script_args.source_folder_path
    replica_dir = script_args.replica_folder_path

    @tl.job(interval=timedelta(seconds=int(script_args.sync_interval)))
    def synchronize_files():
        """Synchronize files in folders in a predetermined interval."""
        for file in os.listdir(source_dir):

            if file in os.listdir(replica_dir):

                if os.path.getmtime(f'{source_dir}\\{file}') > os.path.getmtime(f'{replica_dir}\\{file}'):
                    shutil.copy(f'{source_dir}\\{file}', replica_dir)
                    logger.logger.info(f"{file} has been updated.")

            else:
                shutil.copy(f'{source_dir}\\{file}', replica_dir)
                logger.logger.info(f"{file} was created in replica folder.")

        for file in os.listdir(replica_dir):

            if file not in os.listdir(source_dir):
                os.remove(f"{replica_dir}\\{file}")
                logger.logger.info(f"{file} was removed from replica folder.")

        logger.logger.info("Files are up to date.")

    tl.start(block=True)

# -*- coding: utf-8 -*-
"""Custom logger."""

import logging
import sys
from logging import handlers


class Logger(object):
    """Logging class"""
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # relationship mapping

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(name)s - %(levelname)s: %(message)s'):
        """Initialize logging class."""

        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))

        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')
        th.setFormatter(format_str)

        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.addHandler(th)

# -*- coding: utf-8 -*-

import os.path

from instlatte import Manager

import lascaux
from lascaux.config import config


def new_manager():
    return Manager({
        'sources': [os.path.abspath(os.path.join(os.path.dirname(lascaux.__file__), 'subsystems'))],
        'subsystems': config['subsystems']
    })    

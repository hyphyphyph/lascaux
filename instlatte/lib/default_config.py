import os.path


default_config = {
    'sources': [os.path.join(os.path.abspath(os.path.dirname(__file__)), 'subsystems')],
    'subsystems': {
        'import': {
            'enabled': True
        }
    }
}

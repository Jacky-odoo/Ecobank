#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from glob import glob
from setuptools import find_packages, setup
from os.path import join, dirname


execfile(join(dirname(__file__), 'odoo', 'release.py'))  # Load release variables
lib_name = 'odoo'


def py2exe_datafiles():
    data_files = {}
    data_files['Microsoft.VC90.CRT'] = glob('C:\Microsoft.VC90.CRT\*.*')

    for root, dirnames, filenames in os.walk('odoo'):
        for filename in filenames:
            if not re.match(r'.*(\.pyc|\.pyo|\~)$', filename):
                data_files.setdefault(root, []).append(join(root, filename))

    import babel
    data_files['babel/localedata'] = glob(join(dirname(babel.__file__), 'localedata', '*'))
    others = ['global.dat', 'numbers.py', 'support.py', 'plural.py']
    data_files['babel'] = map(lambda f: join(dirname(babel.__file__), f), others)
    others = ['frontend.py', 'mofile.py']
    data_files['babel/messages'] = map(lambda f: join(dirname(babel.__file__), 'messages', f), others)

    import pytz
    tzdir = dirname(pytz.__file__)
    for root, _, filenames in os.walk(join(tzdir, 'zoneinfo')):
        base = join('pytz', root[len(tzdir) + 1:])
        data_files[base] = [join(root, f) for f in filenames]

    import docutils
    import passlib
    import reportlab
    import requests
    data_mapping = ((docutils, 'docutils'),
                    (passlib, 'passlib'),
                    (reportlab, 'reportlab'),
                    (requests, 'requests'))

    for mod, datadir in data_mapping:
        basedir = dirname(mod.__file__)
        for root, _, filenames in os.walk(basedir):
            base = join(datadir, root[len(basedir) + 1:])
            data_files[base] = [join(root, f)
                                for f in filenames
                                if not f.endswith(('.py', '.pyc', '.pyo'))]

    return data_files.items()


def py2exe_options():
    if os.name == 'nt':
        import py2exe
        return {
            'console': [
                {'script': 'odoo-bin', 'icon_resources': [
                    (1, join('setup', 'win32', 'static', 'pixmaps', 'openerp-icon.ico'))
                ]},
            ],
            'options': {
                'py2exe': {
                    'skip_archive': 1,
                    'optimize': 0,  # Keep the assert running as the integrated tests rely on them.
                    'dist_dir': 'dist',
                    'packages': [
                        'asynchat', 'asyncore',
                        'commands',
                        'dateutil',
                        'decimal',
                        'decorator',
                        'docutils',
                        'email',
                        'encodings',
                        'HTMLParser',
                        'imaplib',
                        'jinja2',
                        'lxml', 'lxml._elementpath', 'lxml.builder', 'lxml.etree', 'lxml.objectify',
                        'mako',
                        'markupsafe',
                        'mock',
                        'ofxparse',
                        'odoo',
                        'openid',
                        'passlib',
                        'PIL',
                        'poplib',
                        'psutil',
                        'pychart',
                        'pydot',
                        'pyparsing',
                        'pyPdf',
                        'pytz',
                        'reportlab',
                        'requests',
                        'select',
                        'smtplib',
                        'suds',
                        'uuid',
                        'vatnumber',
                        'vobject',
                        'win32service', 'win32serviceutil',
                        'xlrd',
                        'xlsxwriter',
                        'xlwt',
                        'xml', 'xml.dom',
                        'pysftp',
                        'zklib',
                        'yaml',
                    ],
                    'excludes': ['Tkconstants', 'Tkinter', 'tcl'],
                }
            },
            'data_files': py2exe_datafiles()
        }
    else:
        return {}


setup(
    name='odoo',
    version=version,
    description=description,
    long_description=long_desc,
    url=url,
    author=author,
    author_email=author_email,
    classifiers=filter(None, classifiers.split('\n')),
    license=license,
    scripts=['setup/odoo'],
    packages=find_packages(),
    package_dir={'%s' % lib_name: 'odoo'},
    include_package_data=True,
    install_requires=[
        'babel >= 1.0',
        'decorator',
        'docutils',
        'feedparser',
        'gevent',
        'Jinja2',
        'lxml',  # windows binary http://www.lfd.uci.edu/~gohlke/pythonlibs/
        'mako',
        'mock',
        'ofxparse',
        'passlib',
        'pillow',  # windows binary http://www.lfd.uci.edu/~gohlke/pythonlibs/
        'psutil',  # windows binary code.google.com/p/psutil/downloads/list
        'psycogreen',
        'psycopg2 >= 2.2',
        'python-chart',
        'pydot',
        'pyparsing',
        'pypdf',
        'pyserial',
        'python-dateutil',
        'python-ldap',  # optional
        'python-openid',
        'pytz',
        'pyusb >= 1.0.0b1',
        'pyyaml',
        'qrcode',
        'reportlab',  # windows binary pypi.python.org/pypi/reportlab
        'requests',
        'suds-jurko',
        'vatnumber',
        'vobject',
        'werkzeug',
        'xlsxwriter',
        'xlwt',
        'pysftp'
    ],
    extras_require={
        'SSL': ['pyopenssl'],
    },
    tests_require=[
        'mock',
    ],
    **py2exe_options()
)

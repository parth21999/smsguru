from setuptools import setup, find_packages

setup(
    name="SMSGuru",
    version="0.1.0",
    packages=find_packages(include=['App_files', 'App_files.*']),
    install_requires=[
        'absl-py==0.1.10',
        'astor==0.6.2',
        'bleach==1.5.0',
        'click==6.7',
        'enum34==1.1.6',
        'Flask==1.0.2',
        'gast==0.2.0',
        'grpcio==1.9.1',
        'gunicorn==19.9.0',
        'html5lib==0.9999999'
        'itsdangerous==0.24',
        'Jinja2==2.10',
        'Markdown==2.6.11',
        'MarkupSafe==1.0',
        'numpy==1.14.0',
        'olefile==0.44',
        'Pillow==4.3.0',
        'protobuf==3.5.1',
        'six==1.11.0',
        'Werkzeug==0.14.1',
        'wikipedia==1.4.0',
        'nltk==3.3.0',
        'duckduckpy==0.2',
        'rake-nltk==1.0.4',
        'google==2.0.2',
        'truecase==0.0.4',
        'requests==2.22.0',
        'Flask-MySQL==1.4.0',
        'mysql-connector-python==8.0.17',
        'googletrans==2.4.0',
        'readability-lxml==0.7.1'
    ]
)
from setuptools import setup

setup(
    name = 'sje',
    version = '1.0.0',
    description = 'Schema JSON Extractor.',
    author = 'Ryan Yuan',
    author_email = 'ryan.yuan@outlook.com',
    packages = ['sje'],
    install_requires = [
        'pytest==5.0.0',
        'PyYAML==5.1.1',
        'sqlparse==0.3.0'
    ],
    entry_points = {
        'console_scripts': [
            'sje = sje.__main__:main'
        ]
    }
)
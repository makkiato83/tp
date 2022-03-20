from setuptools import setup

setup(
    name='tp',
    version='0.1.0',
    py_modules=['tp'],
    install_requires=[
        'Click', 'stem'
    ],
    entry_points={
        'console_scripts': [
            'tp = tp:cli',
        ],
    },
)
from setuptools import setup

setup(
    name='cli',
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        'click',
        'requests',
        'colorama'
    ],
    entry_points = {
        'console_scripts': ['energy_group30=cli:cli']
    },
    packages = ['config', 'utils']
)

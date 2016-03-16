from setuptools import setup

setup(
    name='Top committees in github',
    version='0.1',
    py_modules=['githubcomittees'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        committees=githubcommitters:printTopCommitter
    ''',
)


from setuptools import setup

setup(
    name='restaurapp-back',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
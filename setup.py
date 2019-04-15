from setuptools import setup

setup(
    name='silex',
    version='0.0.2',
    packages=[
        'silex',
        'silex.engines',
        'silex.datatype',
        "silex.queue",
    ],
    url='https://github.com/redstone-project/silex',
    license='MIT',
    author='lightless',
    author_email='lightless@foxmail.com',
    description='silex is an more generic SDK for my self projects.',
    install_requires=[
        "pika"
    ]
)

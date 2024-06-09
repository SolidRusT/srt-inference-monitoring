from setuptools import setup, find_packages

setup(
    name='srt-inference-monitoring',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask==2.3.2',
        'gunicorn==20.1.0',
        'prometheus-client==0.16.0',
        'pyyaml==6.0',
        'requests==2.28.2',
        'APScheduler==3.9.1.post1',
        'redis>=4.3.4'
    ],
    entry_points={
        'console_scripts': [
            'start-monitoring=start:main',
        ],
    },
)

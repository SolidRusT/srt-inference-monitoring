from setuptools import setup, find_packages

setup(
    name='srt-inference-monitoring',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask==2.3.2',
        'gunicorn==22.0.0',
        'prometheus-client==0.16.0',
        'pyyaml==6.0',
        'requests==2.32.2',
        'APScheduler==3.9.1.post1',
        'redis==4.4.4'
    ],
    entry_points={
        'console_scripts': [
            'start-monitoring=app.start:main',
        ],
    },
)

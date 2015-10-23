from setuptools import setup

setup(
    name='gullinkambi',
    version='0.0.1',
    author='Mihir Singh (@citruspi)',
    author_email='mihir.singh@hudl.com',
    packages=['gullinkambi'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'requests'
    ]
)

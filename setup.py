from setuptools import setup

setup(
    name='kambi',
    version='0.0.1',
    author='Mihir Singh (@citruspi)',
    author_email='mihir.singh@hudl.com',
    packages=['kambi'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'requests'
    ],
    scripts=[
        'scripts/kambid'
    ]
)

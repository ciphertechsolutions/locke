from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(name='locke',
      version='0.1.5a6',
      description='A fork of BalBuzard',
      long_description=readme,
      url='https://www.ciphertechsolutions.com/',
      author='Cipher Tech Solutions',
      author_email='ahavens@ciphertechsolutions.com',
      license='BSD',
      packages=['apm', 'liblocke', 'locke', 'patterns', 'transformers'],
      package_data={'transformers': ['data/transforms.db']},
      python_requires='>=3',
      install_requires=[
          'msgpack-python',
          'click',
      ],
      entry_points={
          'console_scripts': [
              'locke=locke.locke:main',
          ],
      },
      zip_safe=False)

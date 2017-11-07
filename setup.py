from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

setup(name='locke',
      version='0.1.5a8',
      description='A fork of BalBuzard',
      long_description=readme,
      url='https://www.ciphertechsolutions.com/',
      author='Cipher Tech Solutions',
      author_email='ahavens@ciphertechsolutions.com',
      license='BSD',
      packages=find_packages(),
      package_data={'locke.transforms': ['data/transforms.db']},
      python_requires='>=3',
      install_requires=[
          'click',
      ],
      entry_points={
          'console_scripts': [
              'locke=locke.locke_main:main',
          ],
      },
      zip_safe=False)

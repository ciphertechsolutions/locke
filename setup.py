from setuptools import setup, find_packages

setup(name='locke',
      version='0.1.5-alpha',
      description='A fork of BulBuzard',
      url='https://www.ciphertechsolutions.com/',
      author='Cipher Tech Solutions',
      author_email='ahavens@ciphertechsolutions.com',
      license='placeholder',
      packages=find_packages(),
      py_modules='locke',
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
      zip_safe=True)

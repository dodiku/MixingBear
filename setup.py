from setuptools import setup

with open('README.md') as f:
    long_description = f.read()


setup(name='mixingbear',
      version='0.0.1',
      description='Automatic beat-mixing of music files',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Topic :: Multimedia :: Sound/Audio :: Mixers'
      ],
      keywords='Automatic beat-mixing of music files. audio analysis',
      url='https://github.com/dodiku/MixingBear',
      author='Dror Ayalon',
      author_email='d.stamail@gmail.com',
      license='MIT',
      packages=['mixingbear'],
      install_requires=[
        'audioowl',
        'pydub>=0.20.0,<0.20.1',
      ],
      include_package_data=True,
      zip_safe=False)

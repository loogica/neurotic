import setuptools

setuptools.setup(name='neurotic',
                 version='',
                 description='',
                 long_description=open('README.markdown').read().strip(),
                 author='',
                 author_email='',
                 url='',
                 packages=['neurotic', 'neurotic/file_monitor'],
                 install_requires=['pytest>=2.2.3', 'coopy>=0.3'],
                 entry_points={
                     'pytest11': ['neurotic = neurotic.report_plugin'],
                     'nose.plugins.0.10' : [
                         'neurotic = neurotic.report_plugin:NeuroticNosePlugin'
                      ],
                     'console_scripts': [
                         'neurotic = neurotic.command_line:main',
                      ]
                 },
                 license='MIT License',
                 keywords='',
                 classifiers=['Development Status :: 4 - Beta',
                              'Intended Audience :: Developers',
                              'License :: OSI Approved :: MIT License',
                              'Operating System :: OS Independent',
                              'Programming Language :: Python',
                              'Programming Language :: Python :: 2.4',
                              'Programming Language :: Python :: 2.5',
                              'Programming Language :: Python :: 2.6',
                              'Programming Language :: Python :: 2.7',
                              'Programming Language :: Python :: 3.0',
                              'Programming Language :: Python :: 3.1',
                              'Topic :: Software Development :: Testing'])

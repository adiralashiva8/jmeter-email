from setuptools import setup, find_packages

filename = 'jmeter_email/version.py'
exec(compile(open(filename, 'rb').read(), filename, 'exec'))

setup(name='jmeter-email',
      version=__version__,
      description='Send email with Jmeter result',
      long_description='Send email with jmeter results, which are created by parsing .jtl or .csv file',
      classifiers=[
          'Programming Language :: Python',
          'Topic :: Software Development :: Testing',
      ],
      keywords='Jmeter report',
      author='Shiva Prasad Adirala',
      author_email='adiralashiva8@gmail.com',
      url='https://github.com/adiralashiva8/jmeter-email',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'pandas'
      ],
      entry_points={
          'console_scripts': [
              'jmeteremail=jmeter_email.runner:main',
          ]
      },
      )
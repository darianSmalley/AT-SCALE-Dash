__author__ = "Darian Smalley"
__copyright__ = "Copyright Darian Smalley (2024)"
__maintainer__ = "Darian Smalley"
__email__ = "dsmalle1@jhu.edu"
__version__ = 0.1

from setuptools import setup, find_packages
import os

module_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    setup(
        name='AT-SACLE Dashboard',
        python_requires='>=3.8',
        version=__version__,
        description='Interactive dashboard for inspecting DED printer log data.',
        long_description=open(os.path.join(module_dir, 'README.md')).read(),
        long_description_content_type='text/markdown',
        url='https://github.com/JHU-Metal-AM/AT-SCALE-Dash',
        author=__author__,
        author_email=__email__,
        license='JHU Academic Software License',
        packages=find_packages(),
        zip_safe=False,
        install_requires=[
            'numpy',
            'plotly',
            'dash',
            'dash-bootstrap-components',
            'pandas',
        ],
        classifiers=['Programming Language :: Python',
                     'Development Status :: 1 - Alpha',
                     'Intended Audience :: Science/Research',
                     'Operating System :: OS Independent',
                     'Topic :: Scientific/Engineering']
    )
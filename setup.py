__import__('setuptools').setup(
    name="eye",
    version="0.0.🖕",
    author="Tony Fast", author_email="tony.fast@gmail.com",
    description="Interactive Notebook Modules.", 
    license="BSD-3-Clause",
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-ipynb'],
    install_requires=['ipython', 'nbconvert'],
    packages=['eye'])

`eye` imports notebooks as Interactive Modules.  With `eye` imports:

* Notebooks can be used as python source.
* The native `importlib.reload` object reloads `eye` modules.
* `eye` provides line level debugging to the source notebook.
* `paramterize` notebooks to makes them `callable`.

## `eye.tests` may be imported


```python
    import eye.tests
    import eye.activate
    from importlib import reload
```


```python
if __name__ == '__main__':
    !python setup.py develop
    !jupyter nbconvert --to markdown readme.ipynb
```

    /Users/tonyfast/anaconda/lib/python3.5/site-packages/setuptools-27.2.0-py3.5.egg/setuptools/dist.py:340: UserWarning: The version specified ('0.0.🖕') is an invalid version, this may not work as expected with newer versions of setuptools, pip, and PyPI. Please see PEP 440 for more details.
    running develop
    running egg_info
    writing eye.egg-info/PKG-INFO
    writing top-level names to eye.egg-info/top_level.txt
    writing dependency_links to eye.egg-info/dependency_links.txt
    reading manifest file 'eye.egg-info/SOURCES.txt'
    writing manifest file 'eye.egg-info/SOURCES.txt'
    running build_ext
    Creating /Users/tonyfast/anaconda/lib/python3.5/site-packages/eye.egg-link (link to .)
    eye 0.0.- is already the active version in easy-install.pth
    
    Installed /Users/tonyfast/eye
    Processing dependencies for eye===0.0.-
    Finished processing dependencies for eye===0.0.-
    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 411 bytes to readme.md



`eye` imports notebooks as Interactive Modules.  With `eye` imports:

* Notebooks can be used as python source.
* The native `importlib.reload` object reloads `eye` modules.
* `eye` provides line level debugging to the source notebook.
* `paramterize` notebooks to makes them `callable`.

## `eye.tests` may be imported


```python
    try:                        import eye.tests.basics
    except ModuleNotFoundError: import eye.activate
    finally:                    import eye.tests.basics
```


```python
if __name__ == '__main__':
    !python setup.py develop
    !jupyter nbconvert --to markdown readme.ipynb
```

    /Users/tonyfast/anaconda/lib/python3.5/site-packages/setuptools-27.2.0-py3.5.egg/setuptools/dist.py:340: UserWarning: The version specified ('0.0.🖕') is an invalid version, this may not work as expected with newer versions of setuptools, pip, and PyPI. Please see PEP 440 for more details.
    running develop
    running egg_info
    writing pbr to eye.egg-info/pbr.json
    writing top-level names to eye.egg-info/top_level.txt
    writing dependency_links to eye.egg-info/dependency_links.txt
    writing eye.egg-info/PKG-INFO
    reading manifest file 'eye.egg-info/SOURCES.txt'
    reading manifest template 'MANIFEST.in'
    writing manifest file 'eye.egg-info/SOURCES.txt'
    running build_ext
    Creating /Users/tonyfast/anaconda/lib/python3.5/site-packages/eye.egg-link (link to .)
    eye 0.0.- is already the active version in easy-install.pth
    
    Installed /Users/tonyfast/eye
    Processing dependencies for eye===0.0.-
    Finished processing dependencies for eye===0.0.-
    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 1582 bytes to readme.md


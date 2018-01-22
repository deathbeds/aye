
`eye` imports notebooks as Interactive Modules.  With `eye` imports:

* Notebooks can be used as python source.
* The native `importlib.reload` object reloads `eye` modules.
* `eye` provides line level debugging to the source notebook.
* `paramterize` notebooks to makes them `callable`.


```python
    import eye.activate
    import readme
```

Imported notebooks are reloadable.


```python
    from importlib import reload
    assert reload(readme) is readme
```

`eye` imports notebooks directly from their json source.


```python
    from inspect import getsource
    assert readme.__file__.endswith('.ipynb')
    assert __import__('nbformat').reads(getsource(readme), 4)
```

`eye.tests` are importable.


```python
    from eye import update_hooks, Notebook
    update_hooks()
    try:                        import eye.tests.test_basics
    except ModuleNotFoundError: update_hooks(Notebook)
    finally:                    import eye.tests.test_basics
    assert eye.tests.test_basics.__complete__ is True
```


```python
if __name__ == '__main__':
#     !python setup.py develop
    !source activate p6 && py.test
    !jupyter nbconvert --to markdown --TemplateExporter.exclude_output=True readme.ipynb
```

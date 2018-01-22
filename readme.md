
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
    !jupyter nbconvert --to markdown --TemplateExporter.exclude_output=True readme.ipynb
```


# coding: utf-8

# `aye` creates tools to load 

# In[1]:


__doc__ = """
This notebook creates a module named `aye`.  `aye` 
allows users to import notebooks as Python modules with _sorta_ improved debugging features.

# Suppressing expressions when importing notebooks

Use the condition 

    __name__ == '__main__'

as a control flow to ignore stay
"""


# ## Updating `sys.path_hooks`
# 
# [Registering path hooks][302], [Import Hooks][imp]
# 
# [302]: https://www.python.org/dev/peps/pep-0302/#id28
# [imp]: https://docs.python.org/3/reference/import.html#import-hooks

# In[90]:


def update_hooks(*loaders):
    """Append custom loaders to the `sys.path_hooks`, they must 
    have a tuple attribute EXTENSION_SUFFIXES to discover the correct path.
    
    _NATIVE_HOOK resides in the global scope to reset the original sys.path_hooks 
    if necessary..
    """
    global _NATIVE_HOOK
    from importlib.machinery import FileFinder
    
    if loaders:
        for i, hook in enumerate(sys.path_hooks):
            __closure__ = getattr(hook, '__closure__', None)
            if __closure__ and issubclass(__closure__[0].cell_contents, FileFinder):
                _NATIVE_HOOK = globals().get('_NATIVE_HOOK', (i, hook))
                sys.path_hooks[i] = FileFinder.path_hook(
                    *_NATIVE_HOOK[1].__closure__[1].cell_contents,
                    *((loader, loader.EXTENSION_SUFFIXES) for loader in loaders
                ))
    else:
        sys.path_hooks[_NATIVE_HOOK[0]] = _NATIVE_HOOK[1]
            
    """https://docs.python.org/3/library/sys.html#sys.path_importer_cache"""
    sys.path_importer_cache.clear()


# `sys.path_importer_cache.clear()`
# 
# 
# [jup]: http://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html#Register-the-hook
# [importable]: https://github.com/tonyfast/importable/blob/master/importable.py#L83

# In[91]:


from IPython.utils.capture import capture_output
from IPython.display import publish_display_data


# In[92]:


from contextlib import contextmanager
@contextmanager
def Import(*loaders, capture=False): 
    """A contextmanager that modifies the sys.path_hooks and returns them 
    to their original state.
    
    """
    if capture:
        with capture_output() as captured:
            update_hooks(*loaders or [Notebook])
            yield captured
            update_hooks()
    else:
        yield update_hooks(*loaders or [Notebook]); update_hooks()


# ## Loaders 
# 
# [Import loaders][load]
# 
# [load]: https://docs.python.org/3/reference/import.html#loaders

# # Notebook Source File Loader

# In[93]:


from importlib.machinery import SourceFileLoader


# The native [`importlib.machinery.SourceFileLoader`](https://docs.python.org/3/library/importlib.html#importlib.machinery.SourceFileLoader) provides the general API to import modules from files.  This API will compile and cache the byte-code like a normal module in __pycache__.
# 
# > The [UML diagram of `eye`](#uml-diagram) illustrates all of the methods provided by the loader.
# 
# `Notebook` uses the [`SourceFileLoader.source_to_code`](https://docs.python.org/3/library/importlib.html#importlib.abc.InspectLoader.source_to_code)
# method to transform the source string into valid python AST.  `Notebook.source_to_code` calls a new method `Notebook.source_to_lines`
# that decodes the string into blocks of iterable source code; `Notebook.source_to_lines` can be used by other 
# methods to customize `Module` imports.
# 
# It is necessary that the `Notebook` __loader__ can `importlib.reload` the modules it produces.
# 
# ## Completeness
# 
# `Notebook.exec_module` catches all errors on the attribute __complete__.  With this approach all notebooks with important and the user can 
# 
#     raise nb.__complete__ 
#     
# to return a __traceback__.  A successful import will `assert nb.__complete__`.

# In[94]:


class Partial(SourceFileLoader):
    """A SourceFileLoader specifically designed for `nbformat.v4` files. The `Notebook`
    loader will create compiled python byte code for better interactive debugging.
    
    """
    def source_to_code(Notebook, data, path, *, _optimize=-1):
        """Introduces `source_to_lines` to the standard import pipeline.
        """
        return super().source_to_code(lines_to_ast(
            Notebook.source_to_lines(Notebook.get_source(Notebook.name))
        ), path, _optimize=_optimize)

    @staticmethod
    def source_to_lines(data:str)->'Iterator[Tuple(Int, Str)]':
        """Transform `NotebookNode.cells`, with `nbformat.v4`, into source code objects
        with the corresponding lines number in source `.ipynb` files.  The `new_decoder` is 
        a `json.decoder` that extracts the line numbers and code blocks from the source file.
        """
        yield 1, data
    
    def exec_module(Notebook, module):
        """exec_module explicitly rewrites _bootstrap_external._LoaderBasics.exec_module
        to pass globals into the import.  
        
        This version of exec_module will always __complete__ if an ImportError is not raised.
        __complete__ may hold an exception.
        """
        from importlib import _bootstrap_external, _bootstrap
        from types import MethodType
        
        module.__doc__ = module.__doc__ or """"""
        module.__complete__ = False
        code = Notebook.get_code(module.__name__)
        code is None and """Raise the expected error.""" and super().exec_module(module)
        try: 
            _bootstrap._call_with_frames_removed(exec, code, module.__dict__, module.__dict__)
            module.__complete__ = True
        except BaseException as Exception: module.__complete__ = Exception
        return module #repr_markdown(module)
    
    __complete__ = False


# In[95]:


class Notebook(Partial):
    """A SourceFileLoader specifically designed for `nbformat.v4` files. The `Notebook`
    loader will create compiled python byte code for better interactive debugging.
    
    """
    EXTENSION_SUFFIXES = '.ipynb',
    
    @staticmethod
    def source_to_lines(data:str)->'Iterator[Tuple(Int, Str)]':
        """Transform `NotebookNode.cells`, with `nbformat.v4`, into source code objects
        with the corresponding lines number in source `.ipynb` files.  The `new_decoder` is 
        a `json.decoder` that extracts the line numbers and code blocks from the source file.
        """
        yield from new_decoder().decode(data)


# ## Decoding `nbformat.v4`
# 
# `NBDecoder` is a custom [`JSONDecoder.parse_object`](https://docs.python.org/3/library/json.html#json.JSONDecoder) that applies special operations on the `NotebookNode.source` and
# `NotebookNode.cells`.  The line numbers must be recorded in the decoder.
# 
# > `nbformat` is not formally called, it is assumed the data structure is valid.

# In[96]:


from json.decoder import WHITESPACE, WHITESPACE_STR
def NBDecoder(s_and_end, strict, scan_once, object_hook, 
              object_pairs_hook, memo=None, _w=WHITESPACE.match, _ws=WHITESPACE_STR):
    from json.decoder import JSONObject
    from nbconvert.filters import comment_lines, indent
    
    doc, id = s_and_end

    object, next = JSONObject((doc, id), strict, scan_once, object_hook, object_pairs_hook, memo=memo, _w=_w, _ws=_ws)
    if 'source' in object:
        type, object = object['cell_type'], object['source']
        object = ''.join(object) if isinstance(object, list) else object            
        id = doc.count('\n', 0, id + doc[id:next].find(object and object.splitlines()[0] or 'source'))
        object = id, (object if type == 'code' else comment_lines(object))
    elif 'cells' in object:
        object = object['cells']

    return object, next

def new_decoder():
    from json.decoder import JSONDecoder
    from json.scanner import py_make_scanner
    decoder = JSONDecoder()
    decoder.parse_object = NBDecoder
    decoder.scan_once = py_make_scanner(decoder)
    return decoder


# # Literate Markdown Tools

# In[97]:


from nbconvert.filters.markdown_mistune import IPythonRenderer, MarkdownWithMath
class Markdown(MarkdownWithMath):
    """A mistune.Markdown object that accumulates the source code in the markdown body.
    """
    def render(Markdown, text):
        from nbconvert.filters import ipython2python
        Markdown.renderer.source = """"""
        return [super().render(text), ipython2python(Markdown.renderer.source)][-1]


# In[98]:


class Renderer(IPythonRenderer):
    """A mistune.Renderer to use with `aye.Markdown`."""
    def __init__(Renderer, *args, **kwargs): 
        Renderer.source = super().__init__(*args, **kwargs) or """"""

    def block_code(Renderer, str, lang=None):
        Renderer.source += '\n' + str
        return super().block_code(str, lang=lang)


# In[99]:


class Literate(Notebook):
    """A loader for literate Markdown notebooks."""
    def source_to_lines(Notebook, data, body=""""""): 
        md = Markdown(Renderer())
        for id, str in super().source_to_lines(data): 
            yield id, (md.render(str), md.renderer.source)[-1]


# In[100]:


class MD(Partial):
    EXTENSION_SUFFIXES = '.md', '.markdown'
    def source_to_lines(Notebook, data, body=""""""): 
        from textwrap import dedent
        from nbconvert.filters import ipython2python
        md = Markdown(Renderer())
        md.render(data)
        yield 1, ipython2python(dedent(md.renderer.source))


# # IPython tools

# # Utilities

# In[101]:


import sys
from importlib import reload

def ast(Notebook): 
    loader = Notebook.__loader__
    return lines_to_ast(loader.source_to_lines(loader.get_source(loader.name)))

def free_expressions(module):
    from collections import OrderedDict
    from ast import Expr, Str, Assign, Module, parse, literal_eval, dump
    dict, assigned = OrderedDict(), list()
    new = Module(body=[])
    for node in module.body:
        if isinstance(node, Expr) and isinstance(node.value, Str):
            params = parse(node.value.s).body
            if params and isinstance(params[0], Assign) and len(params[0].targets) is 1: 
                dict[params[0].targets[0].id] = literal_eval(params[0].value)
                assigned.append(dump(params[0].targets[0]))
        elif isinstance(node, Assign) and node.targets and dump(node.targets[0]) in assigned:
            """Do not append parameterized assigments."""
        else: new.body.append(node)
    return dict, new

def vars_to_sig(vars):
    from inspect import Parameter, Signature
    return Signature([Parameter(str, Parameter.KEYWORD_ONLY, default = vars[str]) for str in vars])


# In[102]:


def copy_module(module):
    from types import ModuleType
    new = ModuleType(module.__name__, module.__doc__)
    new.__dict__.update(module.__dict__)
    return new


# In[103]:


def parameterize(nb):
    module = copy_module(nb)
    AST = ast(module)
    variables, AST = free_expressions(AST)
    for variable in variables: 
        if variable in module.__dict__: module.__dict__.pop(variable)
    
    module.__dict__.update(variables)
    
    def run(**kwargs): 
        module.__dict__.update(kwargs)
        exec(
            compile(AST, module.__file__, 'exec'), 
            module.__dict__, module.__dict__)
        return module
    run._variables = variables
    run.__signature__ = vars_to_sig(variables)
    run.__doc__ = nb.__doc__
    return run


# In[104]:


def lines_to_ast(lines):
    """Transform `lines` of Python source to Python AST with the correct
    lines numbers to the original notebook source.
    """
    from ast import Module, parse, increment_lineno
    from nbconvert.filters import ipython2python
    module = Module(body=[])
    for id, str in lines: module.body.extend(
        increment_lineno(node, id) for node in parse(ipython2python(str)).body)
    return module


# In[105]:


def from_file(path, loader=Notebook, capture=False):
    """from_file loads paths as modules with a specified loader.
    
    >>> m = from_file('aye.ipynb')
    >>> mods = set(dir(__import__('sys').modules))
    >>> assert m.__complete__ is True
    >>> assert m.__name__
    >>> assert len(set(dir(__import__('sys').modules)) - mods) is 0
    """
    from importlib._bootstrap import _init_module_attrs
    from importlib.util import spec_from_file_location, module_from_spec
    from types import ModuleType
    # module = module_from_spec()
    # Create the module by hand to avoid the package name winding up in the sys.modules.
    module = _init_module_attrs(
        spec_from_file_location(path, path, loader=loader(path, path)), ModuleType(path, """"""))
    
    if capture:
        with capture_output() as captured:
            module.__loader__.exec_module(module)
        module.__output__ = captured
    else:
        module.__loader__.exec_module(module)
    return module


# In[106]:


def repr_markdown(module):
    """Attach a [Markdown Formatter][format] to modules loaded by `aye`.
    
    [format]: http://ipython.readthedocs.io/en/stable/api/generated/IPython.core.formatters.html#IPython.core.formatters.MarkdownFormatter
    """
    from types import MethodType
    def _repr_markdown_(module):
        return "`%s`\n\n---\n%s"%(repr(module), module.__doc__ or """""")
    module._repr_markdown_ = MethodType(_repr_markdown_, module)
    return module


# In[108]:


if 1 and __name__ ==  '__main__':
    from IPython import get_ipython
    __import__('doctest').testmod(verbose=2)
    get_ipython().system('jupyter nbconvert --to script --output __init__ aye.ipynb')
    get_ipython().system('source activate p6 && py.test')
    get_ipython().system('pyreverse -o png -p aye -A __init__.py')
    get_ipython().system('ipython -m pydoc -- -w aye')
    get_ipython().system('mv aye.html ../docs/index.html')


# # Permissive Markdown Source
# 
# [Transform the full block][transform]
# 
# [transform]: http://ipython.readthedocs.io/en/stable/config/inputtransforms.html#transforming-a-full-block

# In[111]:


from IPython.core.inputtransformer import InputTransformer

class Transformer(__import__('collections').UserList, InputTransformer):
    push = __import__('collections').UserList.append        
    def reset(Transformer): 
        source, Transformer.data = '\n'.join(Transformer), []
        return Markdown(Renderer()).render(source)


# ### Indenting Code

# In[70]:


def register_transforms(ip=None):
    from IPython import get_ipython
    global _NATIVE_TRANSFORM
    ip = ip or get_ipython()
    _NATIVE_TRANSFORM = globals().get('_NATIVE_TRANSFORM', ip.input_transformer_manager)
    ip.input_transformer_manager.logical_line_transforms = []
    ip.input_transformer_manager.physical_line_transforms = []
    ip.input_transformer_manager.python_line_transforms = [Transformer()]


# In[74]:


if __name__ == '__main__':
    nb = from_file('aye.ipynb', capture=True)

    f = parameterize(nb)
    

    m = f(x=42)


#     from ipywidgets import interact
# 
#     interact(f)
# 
#     [publish_display_data(object.data) for object in nb.__output__.outputs];

# from aye import update_hooks, Notebook
# update_hooks(Notebook)
# 
# 
# import mod_from_nb
# 
# mod_from_nb.__complete__

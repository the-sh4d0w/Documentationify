# @Sh4d0w
import importlib
import inspect
import os
import sys
import time


def document(path: str) -> None:
    r"""Creates a .txt-file with the name '[original-file-name]-Documentation.txt'.

    Usage:
     >>> document('C:\Users\JohnDoe\Desktop\Test.py')
     Created documentation in C:\Users\JohnDoe\Desktop\Test-Documentation.txt.
    """
    if not path:
        os._exit(0)
    elif not (path.endswith("py") or path.endswith("pyw")):
        raise Exception("Your file is not a python file.")
    documentation = ""
    try:
        spec = importlib.util.spec_from_file_location(
            os.path.basename(path).split(".")[0], path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
    except AttributeError:
        raise Exception("Your file path seems to be invalid.")
    if [i for _, i in inspect.getmembers(foo) if inspect.ismodule(i)]:
        documentation += "The following modules are imported:\n"
        for _, obj in inspect.getmembers(foo):
            if inspect.ismodule(obj):
                documentation += f" - {obj.__name__}\n"
        documentation += "\n"
    for _, obj in inspect.getmembers(foo):
        if inspect.isclass(obj):
            cls_name = f"class {obj.__name__}:\n"
            cls_doc_string = f" Description by developer: {obj.__doc__}\n"
            methods = " This class has the following methods:\n\n"
            for _, obj in inspect.getmembers(obj):
                if inspect.isfunction(obj):
                    name = f"  method {obj.__name__}:\n"
                    doc_string = f"   Description by developer: {obj.__doc__}\n"
                    try:
                        parameters = f"   Takes {obj.__code__.co_argcount - 1} parameter(s){(' ' if  obj.__code__.co_argcount > 0 else '') + ' and '.join([i + ' of type ' + str(obj.__annotations__[i]) for i in obj.__code__.co_varnames[:obj.__code__.co_argcount] if i != 'self'])}.\n"
                    except:
                        parameters = f"   Takes {obj.__code__.co_argcount - 1} parameter(s){(' ' if  obj.__code__.co_argcount > 0 else '') + ' and '.join([i for i in obj.__code__.co_varnames[:obj.__code__.co_argcount] if i != 'self'])}.\n"
                    try:
                        returntype = f"   Returns {obj.__annotations__['return']}.\n\n"
                    except:
                        returntype = f"   Return-type not specified by developer.\n\n"
                    methods += name + doc_string + parameters + returntype
            documentation += cls_name + cls_doc_string + methods
        elif inspect.isfunction(obj):
            name = f"function {obj.__name__}:\n"
            doc_string = f" Description by developer: {obj.__doc__}\n"
            try:
                parameters = f" Takes {obj.__code__.co_argcount} parameter(s){(' ' if  obj.__code__.co_argcount > 0 else '') + ' and '.join([i + ' of type ' + str(obj.__annotations__[i]) for i in obj.__code__.co_varnames[:obj.__code__.co_argcount]])}.\n"
            except:
                parameters = f" Takes {obj.__code__.co_argcount} parameter(s){(' ' if  obj.__code__.co_argcount > 0 else '') + ' and '.join([i for i in obj.__code__.co_varnames[:obj.__code__.co_argcount]])}.\n"
            try:
                returntype = f" Returns {obj.__annotations__['return']}.\n\n"
            except:
                returntype = f" Return-type not specified by developer.\n\n"
            documentation += name + doc_string + parameters + returntype
    with open(f"{path.replace('.py', '').replace('.pyw', '')}-Documentation.txt", "w") as f:
        f.write(documentation)
    print(
        f"Created documentation in {path.replace('.py', '').replace('.pyw', '')}-Documentation.txt.")


if __name__ == "__main__":
    print(" Please note that for creating an useful documentation your help is needed. Use docstrings (PEP 257: https://www.python.org/dev/peps/pep-0257/) and function annotations (PEP 3107: https://www.python.org/dev/peps/pep-3107/).\n Python executes files when importing them. To create the documentation the file is imported so make sure that you don't have code that will be executed. You can do that by checking if __name__ == '__main__'.\nIf you don't want to continue just press enter without entering a path.\n")
    path = input(
        "Please give a path to the file you want to create a documentation for: ")
    document(path)

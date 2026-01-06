import importlib
import pkgutil
import inspect
from steganalysis.core.base import StegPlugin

def load_plugins(package):
    plugins = []

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package.__name__}.{module_name}")

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, StegPlugin)      
                and obj is not StegPlugin          ):
                plugins.append(obj())             
    return plugins

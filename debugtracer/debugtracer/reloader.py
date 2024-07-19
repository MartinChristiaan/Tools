import importlib
import os
import sys
from pathlib import Path


class ModuleReloader:
    def __init__(self) -> None:
        self.module_timestamps = {}
        self.module_keys = self.get_module_keys()
        self.get_timestamps_modules_last_changed()
        self.imported_modules = {}

    def get_timestamps_modules_last_changed(self):
        python_files = list(Path(os.getcwd()).glob("**/*.py"))
        for python_file in python_files:
            self.module_timestamps[python_file] = python_file.stat().st_mtime

    def reload_is_needed(self):
        should_reload = False
        for module, timestamp in self.module_timestamps.items():
            if timestamp != module.stat().st_mtime:
                should_reload = True
                self.module_timestamps[module] = module.stat().st_mtime
        return should_reload

    def get_module_keys(self):
        keys = []
        python_files = list(Path(os.getcwd()).glob("**/*.py"))
        for python_file in python_files:
            key = (
                str(python_file)
                .replace(os.getcwd(), "")
                .replace("/", ".")
                .replace(".py", "")
            )[1:]
            keys.append(key)
        return keys

    def get_imported_modules(self):
        modules = []
        for key, mod in list(sys.modules.items()):
            if key in self.module_keys:
                modules.append(mod)
        return modules

    def import_or_reload_module(self, module_key):
        if module_key in self.imported_modules:
            if self.reload_is_needed():
                imported_modules = self.get_imported_modules()
                for m in imported_modules:
                    importlib.reload(m)
            imported_module = self.imported_modules[module_key]
        else:
            imported_module = importlib.import_module(module_key)
            self.imported_modules[module_key] = imported_module
        return imported_module

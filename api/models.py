import importlib
import os


def load_models():
    root_dir = os.path.dirname(__file__)
    path = f'{root_dir}/domain'
    files = os.scandir(path)
    domain_directories = [file for file in files if file.is_dir()]

    print("domain directories: ", domain_directories)

    for domain_directory in domain_directories:
        root_dir = os.path.dirname(__file__)
        path = f'{root_dir}/domain/{domain_directory.name}'
        files = os.listdir(path)
        model_files = [file for file in files if file.endswith('_model.py')]
        for file in model_files:
            module_name = file[:-3]  # Remove the .py extension
            full_module_name = f'api/domain/{domain_directory.name}/{module_name}'.replace('/', '.')
            model_module = importlib.import_module(full_module_name)
            if not model_module:
                raise Exception(f"Error loading app models, Module {full_module_name}")

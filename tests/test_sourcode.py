import pytest
import os
from pathlib import Path
from kube_hound.frontend.config import ApplicationConfig

def print_directory_tree(path, indent=''):
    """Recursively print the contents of a directory in a tree-like structure."""
    contents = os.listdir(path)
    for item in contents:
        item_path = Path(path)/ Path(item)
        if os.path.isfile(item_path):
            # Print file name
            print(indent + '- ' + item)
        elif os.path.isdir(item_path):
            # Print directory name
            print(indent + '+ ' + item)
            print_directory_tree(item_path, indent + '  ')  # Recursively print contents of subdirectory


def test_sourcecode_path():
    """Check that the parsed sourcecode path actually returns the local directory with all of its contents."""
    skip_file_types = [".jpg", ".png", ".gif"]

    """Check online-boutique."""
    #get parent directory
    context = os.getcwd()
    #build path strings for necessary to build ApplicationObject
    path_string = Path(context)/Path('test_files/online-boutique/application')
    conf_path_string = Path(context)/Path('test_files/online-boutique/online-boutique-config.yaml')


    context_path = Path(path_string).resolve().absolute()
    configpath= Path(conf_path_string).resolve().absolute()
    config = ApplicationConfig(context_path)
    config.load_config_from_file(configpath)
    config.repositories = config.acquire_application()
    sourcecode_dir = config.acquire_sourcecodes(config.repositories)

    # print directory tree
    for keys in sourcecode_dir:
        print_directory_tree(sourcecode_dir[keys])

        for file_name in os.listdir(sourcecode_dir[keys]):
            if os.path.isfile(Path(sourcecode_dir[keys])/Path( file_name)):
                if any(file_name.endswith(file_type) for file_type in skip_file_types):
                    # Skip files with specified extensions
                    continue
                with open(Path(sourcecode_dir[keys])/Path(file_name), "r") as file:
                    file_contents = file.read()
                    print("File:", file_name)
                    print("Source Code:")
                    print(file_contents)
                    print("-----")
        assert(os.path.isdir(sourcecode_dir[keys]))

    """Check sock-shop."""
    #get parent directory
    context = os.getcwd()

    #build path strings for necessary to build ApplicationObject
    path_string = Path(context)/Path('test_files/sock-shop/application')
    conf_path_string = Path(context)/Path('test_files/sock-shop/sock-shop-config.yaml')
    context_path = Path(path_string)
    configpath= Path(conf_path_string)
    config = ApplicationConfig(context_path)
    config.load_config_from_file(configpath)
    config.repositories = config.acquire_application()
    sourcecode_dir = config.acquire_sourcecodes(config.repositories)

    #print directory tree
    for keys in sourcecode_dir:
        print_directory_tree(sourcecode_dir[keys])

        for file_name in os.listdir(sourcecode_dir[keys]):
            if os.path.isfile(Path(sourcecode_dir[keys])/Path(file_name)):
                if any(file_name.endswith(file_type) for file_type in skip_file_types):
                    # Skip files with specified extensions
                    continue
                with open(Path(sourcecode_dir[keys])/Path(file_name), "r") as file:
                    file_contents = file.read()
                    print("File:", file_name)
                    print("Source Code:")
                    print(file_contents)
                    print("-----")
        assert(os.path.isdir(sourcecode_dir[keys]))

    """Check mock-app. Excecute after cloning the mock-application files locally"""

    """
    # get parent directory
    context = os.getcwd()
    # build path strings for necessary to build ApplicationObject
    path_string = Path(context)/ Path('test_files/mock-application/application')
    conf_path_string = Path(context)/Path('test_files/mock-application/mock-config.yaml')
    context_path = Path(path_string)
    configpath = Path(conf_path_string)
    config = ApplicationConfig(context_path)
    config.load_config_from_file(configpath)
    config.repositories = config.acquire_application()
    sourcecode_dir = config.acquire_sourcecodes(config.repositories)

    # print directory tree
    for keys in sourcecode_dir:
        print_directory_tree(sourcecode_dir[keys])

        for file_name in os.listdir(sourcecode_dir[keys]):
          if os.path.isfile(Path(sourcecode_dir[keys])/Path(file_name)):
                if any(file_name.endswith(file_type) for file_type in skip_file_types):
                    # Skip files with specified extensions
                    continue
                with open(Path(sourcecode_dir[keys])/Path(file_name), "r") as file:
                    file_contents = file.read()
                    print("File:", file_name)
                    print("Source Code:")
                    print(file_contents)
                    print("-----")
        assert(os.path.isdir(sourcecode_dir[keys]))  """
import pytest
import os
from pathlib import Path
import yaml
from kube_hound.frontend.config import ApplicationConfig
from kube_hound.hound import Hound
from loguru import logger

def print_directory_tree(path, indent=''):
    """Recursively print the contents of a directory in a tree-like structure."""
    contents = os.listdir(path)
    for item in contents:
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            print(indent + '- ' + item)  # Print file name
        elif os.path.isdir(item_path):
            print(indent + '+ ' + item)  # Print directory name
            print_directory_tree(item_path, indent + '  ')  # Recursively print contents of subdirectory


def test_sourcecode_path():
    """Check that the parsed sourcecode path actually returns the local directory with all of its contents."""


    #get parent directory
    context = os.path.dirname(os.getcwd())
    #build path strings for necessary to build ApplicationObject
    path_string = os.path.join(context, 'test_files/online-boutique/application')
    conf_path_string = os.path.join(context, 'test_files/online-boutique/online-boutique-config.yaml')
    context_path = Path(path_string)
    configpath= Path(conf_path_string)
    config = ApplicationConfig(context_path)
    config.load_config_from_file(configpath)
    config.repositories = config.acquire_application()
    sourcecode_dir = config.acquire_sourcecodes(config.repositories)

    #print directory tree
    for keys in sourcecode_dir:
        print_directory_tree(sourcecode_dir[keys])


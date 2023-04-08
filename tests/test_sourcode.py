import pytest
import os
from pathlib import Path
import yaml
from kube_hound.frontend.config import ApplicationConfig
from kube_hound.hound import Hound
from loguru import logger

def test_sourcecode_path():
    path = Path('/home/thomas/kubehound/kube-hound/test_files/online-boutique/application')
    configpath= Path('/home/thomas/kubehound/kube-hound/test_files/online-boutique/online-boutique-config.yaml')
    pol = ApplicationConfig(path)
    pol.load_config_from_file(configpath)
    lol = pol.acquire_sourcecodes()

    for keys in lol:
        contents = os.listdir(lol[keys])
        logger.info(contents)


from pathlib import Path
import hcl2
import os
from typing import Dict, List, Optional

from kube_hound.frontend.parsers.abstractparser import ApplicationParser
from kube_hound.frontend.repositories import Repository
from kube_hound.applicationobject import ApplicationObject


class TerraformParser(ApplicationParser):

    def __init__(self, context: Repository, terraform_file: Path, services: Dict):
        self.context = context
        self.context_path = context.get_local_path()
        self.config_file: Path = terraform_file
        self.services = services

    def parse(self) -> List[ApplicationObject]: 
        
        terraform_config = (
            self.context_path/self.config_file).resolve().absolute()

        with open(terraform_config, 'r') as f:
            terraform_object = hcl2.load(f)

        return [ApplicationObject('terraform', self.config_file, data={
            'cache': terraform_object
        })]
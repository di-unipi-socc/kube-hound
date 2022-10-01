import os
from pathlib import Path
from typing import Dict
import yaml
from loguru import logger

from k8spurifier.frontend.repositories import GitRemoteRepository, \
    LocalFolderRefRepository, Repository


# TODO add direct object passing
class ApplicationConfig():
    def __init__(self, context: Path):
        self.context = context
        self.config_object: Dict = {}

    def load_config_from_file(self, config_path: Path):
        config = config_path.resolve().absolute()
        with open(config, 'r') as f:
            self.config_object = yaml.safe_load(f.read())

        # TODO object validation

    def acquire_application(self) -> Dict[str, Repository]:
        logger.info('acquiring the application...')

        if 'repositories' not in self.config_object:
            raise KeyError(
                "The repositories key not found in the config object")

        if not self.context.exists():
            logger.warning(
                f'the specified context does not exists, creating the directory {self.context}')
            os.makedirs(self.context)

        if not self.context.is_dir():
            raise ValueError('The context must be a directory')

        out_repositories: Dict[str, Repository] = {}
        repositories = self.config_object['repositories']
        for repository_name in repositories:
            repository_description = repositories[repository_name]

            if 'git' in repository_description:
                git_url = repository_description['git']
                git_repo = GitRemoteRepository(git_url)
                git_repo.acquire(self.context)
                git_repo.name = repository_name
                out_repositories[repository_name] = git_repo
            elif 'src' in repository_description:
                src_path = self.context / Path(repository_description['src'])
                local_repo = LocalFolderRefRepository(str(src_path))
                local_repo.name = repository_name
                out_repositories[repository_name] = local_repo

        logger.info('finished application acquisition')
        return out_repositories

    def services(self):
        """
        Returns the application services
        """
        if 'services' not in self.config_object:
            raise KeyError('No objects found in the config object')
        return self.config_object['services']

    def deployment(self):
        """
        Returns the application deployment
        """
        if 'deployment' not in self.config_object:
            raise KeyError('No deployment found in the config object')
        return self.config_object['deployment']

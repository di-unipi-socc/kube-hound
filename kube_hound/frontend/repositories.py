import abc
import os
from pathlib import Path
import shutil
from typing import Collection
import git
from loguru import logger


class RepositoryNotAcquiredException(Exception):
    pass


class RepositoriesLocalFolderManager:
    """
    Repositories local folder manager
    """

    def __init__(self, basedir: Path = Path('/tmp'),
                 prefix: str = 'kube-hound') -> None:
        if not isinstance(basedir, Path):
            raise TypeError('basedir has to be a Path object')
        if not isinstance(prefix, str):
            raise TypeError('prefix has to be a str object')

        self.base_path = basedir
        self.prefix = prefix
        self.counter = 0

    def get_new_dir(self) -> Path:
        """
        Get a new unique folder to store the repositories
        """
        new_path = self.base_path / f'{self.prefix}-{self.counter}'
        self.counter += 1
        return new_path


class Repository(metaclass=abc.ABCMeta):
    """
    Abstract Repository class

    A Repository is any folder that can be acquired and copied locally.
    This includes, for example, folders in a git repository or local folders.
    """

    @ abc.abstractmethod
    def get_local_path(self) -> Path: pass

    @ abc.abstractmethod
    def get_name(self) -> str: pass

    def __repr__(self) -> str:
        return f"Repository({self.get_local_path().name})"

    def get_artifacts_by_regex(self, regex: str, recursive=False) -> Collection[Path]:
        """
        Get list of files in a repository by regex.

        Searches in the repository for all the files matching the regex path.
        The regex must represent a relative directory pattern.

        If any resulting file is outside the repository, raises ValueError
        """
        repository_path = self.get_local_path()

        if recursive:
            files = repository_path.rglob(regex)
        else:
            files = repository_path.glob(regex)

        # TODO check that the file is indeed in the repository

        files_filtered = filter(lambda x: not x.is_dir(), files)

        return list(files_filtered)


class LocalFolderRefRepository(Repository):
    """
    Repository that is a reference to a local folder
    The local folder is left unchanged
    """

    def __init__(self, resource_locator: str) -> None:
        source_dir = Path(resource_locator).absolute().resolve()

        if not source_dir.exists():
            raise ValueError('source folder must exists')

        if not source_dir.is_dir():
            raise ValueError('source folder must be a directory')

        self.local_path = source_dir
        self.name = source_dir.name

    def get_local_path(self) -> Path:
        return self.local_path

    def get_name(self) -> str:
        return self.name


class LocalFolderRepository(Repository):
    """
    Repository that is a copy of a local folder to an internal folder
    """

    def acquire(self, resource_locator: str, destination_dir: Path) -> None:
        # check for source folder
        source_dir = Path(resource_locator)

        if not source_dir.is_dir():
            raise ValueError('source folder must be a directory')

        if not source_dir.exists():
            raise ValueError('source folder must exists')

        # check for destination folder
        if not destination_dir.is_dir():
            raise ValueError('local_folder must be a directory')

        if destination_dir.exists():
            raise ValueError('local_folder must not already exists')

        # create the destination folder
        destination_dir.mkdir(parents=True)

        # copy all the files from source to destination
        shutil.copy(source_dir, destination_dir)

        self.local_path = destination_dir
        self.name = self.local_path.name

    def get_local_path(self) -> Path:
        return self.local_path

    def get_name(self) -> str:
        return self.name


class GitRemoteRepository(Repository):
    def __init__(self, remote_url: str):
        self.remote_url = remote_url
        self.acquired = False

    def acquire(self, dst_folder: Path):
        self.name = self._get_remote_name()
        dst_folder = dst_folder.absolute().resolve()
        self.local_path = dst_folder / Path(self.name)

        # check if folder already exists
        if self.local_path.exists():
            logger.info(
                f'attempting to git clone the repository {self.local_path.name}, '
                'but a folder with the '
                'same name already exists, skipping')
            self.acquired = True
            return
        logger.info(f'cloning repository {self.name} into {dst_folder}')
        git.Git(dst_folder).clone(self.remote_url)
        self.acquired = True

    def get_local_path(self) -> Path:
        if not self.acquired:
            raise RepositoryNotAcquiredException()
        return self.local_path

    def get_name(self) -> str:
        return self.name

    def _get_remote_name(self) -> str:
        return os.path.splitext(os.path.basename(self.remote_url))[0]

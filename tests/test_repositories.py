from pathlib import Path
import pytest
from kube_hound.frontend.repositories import LocalFolderRefRepository, \
    Repository


def test_repository_not_instantiable():
    with pytest.raises(TypeError):
        _ = Repository()


def test_local_folder_repo():
    test_path = './test_files'
    repo = LocalFolderRefRepository(test_path)
    assert repo.get_local_path() == Path(test_path).absolute().resolve()


def test_local_folder_repo_exceptions():
    with pytest.raises(ValueError):
        _ = LocalFolderRefRepository('./test_files/test.yaml')

    with pytest.raises(ValueError):
        _ = LocalFolderRefRepository('./does_not_exists')


def test_repository_repr():
    test_path = './test_files'
    repo = LocalFolderRefRepository(test_path)
    assert repr(repo) == 'Repository(test_files)'

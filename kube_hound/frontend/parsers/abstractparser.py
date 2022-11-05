import abc
from typing import List
from kube_hound.applicationobject import ApplicationObject


class ApplicationParser(metaclass=abc.ABCMeta):
    """
    The ApplicationParser class is an abstract base class that provides
    a common interface for all the application parsers.

    All parsers must employ a best effort approach to parsing, providing as much
    data as possible, while silently failing if the parsing cannot be succeded.
    """

    @ abc.abstractmethod
    def parse(self) -> List[ApplicationObject]: pass
    """
    The parse() method implements parsing of an object into a (possibly empty)
    list of ApplicationObject objects.
    """

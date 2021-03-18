from abc import abstractmethod
from typing import Callable, Union

from models.news_article import NewsArticle


class PipelineStage:
    """
    A singular stage in the data pipeline

    Contains a list of listeners that are called upon stage completion
    """
    def __init__(self):
        self._listeners: [Callable[[NewsArticle], None]] = []

    def register_listener(self, callback: Callable[[NewsArticle], None]):
        """
        :param callback: A function that is called when this stage completes
        """
        self._listeners.append(callback)


    def emit(self, to_emit: [NewsArticle]):
        """
        Call all listeners, signifying termination of this stage
        """
        for l in self._listeners:
            l(to_emit)


    def process(self, to_process: [NewsArticle]):
        self.emit([self._process_one(x) for x in to_process])
        self.destroy()

    @abstractmethod
    def _process_one(self, to_process: NewsArticle) -> NewsArticle:
        raise NotImplementedError

    @abstractmethod
    def start(self):
        """
        Force run this pipeline stage

        Should only be called from first stage
        """
        raise NotImplementedError

    @abstractmethod
    def destroy(self):
        """
        Perform any needed cleanup for the stage
        """

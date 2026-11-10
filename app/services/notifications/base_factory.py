from abc import ABC, abstractmethod


class NotificationFactory(ABC):

    @abstractmethod
    def create_notification(self, **kwargs):
        pass
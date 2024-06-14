from typing import Protocol, Union, List


class MessagingProtocol(Protocol):
    def send_message(to: str, message: str) -> bool:
        pass

    def receive_message() -> Union[str, None]:
        pass


class InMemoryMessaging(MessagingProtocol):
    def __init__(self) -> None:
        self.messages: List[dict] = list()

from __future__ import annotations
from abc import ABC, abstractmethod


class BaseSmsGateway(ABC):
    @abstractmethod
    def send_sms(self, phone_number: str, message: str) -> bool:
        raise NotImplementedError


class ConsoleSmsGateway(BaseSmsGateway):
    def send_sms(self, phone_number: str, message: str) -> bool:
        print(f"[SMS] To: {phone_number} | Message: {message}")
        return True


def get_sms_gateway() -> BaseSmsGateway:
    return ConsoleSmsGateway()

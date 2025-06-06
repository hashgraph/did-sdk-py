from dataclasses import dataclass
from typing import ClassVar

from hedera import PublicKey

from .....did.types import SupportedKeyType
from .....utils.encoding import b58_to_bytes, bytes_to_b58
from ....utils import is_owner_event_id_valid
from ..hcs_did_event import HcsDidEvent
from ..hcs_did_event_target import HcsDidEventTarget


@dataclass
class HcsDidUpdateDidOwnerEvent(HcsDidEvent):
    id_: str
    controller: str
    public_key: PublicKey
    type_: SupportedKeyType
    event_target: ClassVar[HcsDidEventTarget] = HcsDidEventTarget.DID_OWNER

    def __post_init__(self):
        if not is_owner_event_id_valid(self.id_):
            raise Exception("Event ID is invalid. Expected format: {did}#did-root-key")

    def get_owner_def(self):
        return {
            "id": self.id_,
            "type": self.type_,
            "controller": self.controller,
            "publicKeyBase58": bytes_to_b58(bytes(self.public_key.toBytesRaw())),
        }

    @classmethod
    def from_json_payload(cls, payload: dict):
        event_json = payload[cls.event_target]
        match event_json:
            case {"id": id_, "type": type_, "controller": controller, "publicKeyBase58": public_key_base58}:
                public_key = PublicKey.fromBytes(b58_to_bytes(public_key_base58))
                return cls(id_=id_, type_=type_, controller=controller, public_key=public_key)
            case _:
                raise Exception(f"{cls.__name__} JSON parsing failed: Invalid JSON structure")

    def get_json_payload(self) -> dict:
        return {self.event_target: self.get_owner_def()}

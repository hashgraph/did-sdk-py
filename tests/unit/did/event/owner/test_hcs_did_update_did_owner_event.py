import pytest

from did_sdk_py.did.hcs.events.hcs_did_event_target import HcsDidEventTarget
from did_sdk_py.did.hcs.events.owner.hcs_did_update_did_owner_event import HcsDidUpdateDidOwnerEvent

from ...common import IDENTIFIER_2


@pytest.fixture
def event(test_key):
    return HcsDidUpdateDidOwnerEvent(
        f"{IDENTIFIER_2}#did-root-key", IDENTIFIER_2, test_key.public_key, test_key.key_type
    )


class TestHcsDidUpdateDidOwnerEvent:
    def test_target(self, event):
        """Targets DIDOwner"""
        assert event.event_target == HcsDidEventTarget.DID_OWNER

    def test_throws_if_id_not_valid(self, test_key):
        """Throws error if id is not valid"""
        with pytest.raises(Exception, match="Event ID is invalid. Expected format: {did}#did-root-key"):
            HcsDidUpdateDidOwnerEvent(IDENTIFIER_2, IDENTIFIER_2, test_key.public_key, test_key.key_type)

    def test_get_id(self, event):
        """returns id that was passed via constructor"""
        assert event.id_ == f"{IDENTIFIER_2}#did-root-key"

    def test_get_type(self, event, test_key):
        """returns key type"""
        assert event.type_ == test_key.key_type

    def test_get_controller(self, event):
        """returns IDENTIFIER_2 passed via constructor"""
        assert event.controller == IDENTIFIER_2

    def test_get_publickey_base64(self, event, test_key):
        """Returns base58 encoded publicKey"""
        assert event.get_owner_def()["publicKeyBase58"] == test_key.public_key_base58

    def test_to_json_tree(self, event, test_key):
        """returns event JSON tree"""
        assert event.get_json_payload() == {
            "DIDOwner": {
                "controller": IDENTIFIER_2,
                "id": f"{IDENTIFIER_2}#did-root-key",
                "publicKeyBase58": test_key.public_key_base58,
                "type": test_key.key_type,
            }
        }

import pytest

from did_sdk_py.did.did_error import DidException
from did_sdk_py.did.hedera_did import HederaDid

from .common import PRIVATE_KEY


class TestHederaDid:
    def test_builds_with_private_key_only(self, mock_client_provider):
        """Successfully builds HederaDid with private key only"""
        did = HederaDid(mock_client_provider, private_key_der=PRIVATE_KEY.toStringDER())

        assert did.identifier is None
        assert did._client == mock_client_provider.get_client()
        assert did.topic_id is None

    def test_builds_identifier_only(self, mock_client_provider):
        """Successfully builds HederaDid with identifier only"""
        identifier = "did:hedera:testnet:z6MkgUv5CvjRP6AsvEYqSRN7djB6p4zK9bcMQ93g5yK6Td7N_0.0.29613327"

        did = HederaDid(mock_client_provider, identifier=identifier)

        assert did.identifier == identifier
        assert did._client == mock_client_provider.get_client()
        assert did.topic_id == "0.0.29613327"
        assert did.network == "testnet"

    @pytest.mark.parametrize(
        ("identifier"),
        [
            "",
            "invalidDid1",
            "did:invalid",
            "did:invalidMethod:8LjUL78kFVnWV9rFnNCTE5bZdRmjm2obqJwS892jVLak_0.0.24352",
            "did:hedera:invalidNetwork:8LjUL78kFVnWV9rFnNCTE5bZdRmjm2obqJwS892jVLak_0.0.24352",
            "did:hedera:testnet:invalidAddress_0.0.24352_1.5.23462345",
            "did:hedera:testnet_1.5.23462345",
            "did:hedera:testnet:z6Mk8LjUL78kFVnWV9rFnNCTE5bZdRmjm2obqJwS892jVLak:unknown:parameter=1_missing",
            "did:hedera:testnet:z6Mk8LjUL78kFVnWV9rFnNCTE5bZdRmjm2obqJwS892jVLak_0.0.1=1",
            "did:hedera:testnet:z6Mk8LjUL78kFVnWV9rFnNCTE5bZdRmjm2obqJwS892jVLak:hedera:testnet:fid",
            "did:hedera:testnet:z6Mk8LjUL78kFVnWV9rFnNCTE5bZdRmjm2obqJwS892jVLak:unknownPart_0.0.1",
            "did:notHedera:testnet:z6Mk8LjUL78kFVnWV9rFnNCTE5bZdRmjm2obqJwS892jVLak_0.0.1",
        ],
    )
    def test_parse_invalid_identifier_throws_error(self, mock_client_provider, identifier):
        """throws error if passed identifier is invalid"""
        with pytest.raises(Exception):  # noqa: B017
            HederaDid(mock_client_provider, identifier=identifier)

    def test_throws_topic_id_missing(self, mock_client_provider):
        """throws error if topicId missing"""
        with pytest.raises(DidException, match="DID string is invalid: topic ID is missing"):
            HederaDid(mock_client_provider, "did:hedera:testnet:z87meAWt7t2zrDxo7qw3PVTjexKWReYWS75LH29THy8kb")

    def test_errors_invalid_method_name(self, mock_client_provider):
        """throws error if invalid method name"""
        with pytest.raises(DidException, match="DID string is invalid: invalid method name: hashgraph"):
            HederaDid(mock_client_provider, "did:hashgraph:testnet:z87meAWt7t2zrDxo7qw3PVTjexKWReYWS75LH29THy8kb_0.0.1")

    def test_error_invalid_hedera_network(self, mock_client_provider):
        """throws error if Invalid Hedera network"""
        with pytest.raises(DidException, match="DID string is invalid. Invalid Hedera network."):
            HederaDid(mock_client_provider, "did:hedera:nonetwork:z87meAWt7t2zrDxo7qw3PVTjexKWReYWS75LH29THy8kb_0.0.1")

    def test_error_invalid_id_string(self, mock_client_provider):
        """throws error if Invalid id string"""
        with pytest.raises(DidException, match="DID string is invalid. ID holds incorrect format"):
            HederaDid(mock_client_provider, 'did:hedera:testnet:z6Mkabcd_0.0.1"')

    def test_parse(self, mock_client_provider):
        """should get array with NetworkName, topicId and didIdString"""
        did = HederaDid(
            mock_client_provider, identifier="did:hedera:testnet:z87meAWt7t2zrDxo7qw3PVTjexKWReYWS75LH29THy8kb_0.0.1"
        )

        assert did.network == "testnet"
        assert did.topic_id == "0.0.1"

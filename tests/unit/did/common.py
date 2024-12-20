from hedera import PrivateKey

from did_sdk_py.utils.encoding import multibase_encode

NETWORK = "testnet"
DID_TOPIC_ID_1 = "0.0.2"
DID_TOPIC_ID_2 = "0.0.3"
DID_TOPIC_ID_3 = "0.0.29613327"
PRIVATE_KEY = PrivateKey.generate()

PRIVATE_KEY_2 = PrivateKey.generate()

PUBLIC_KEY_DER = multibase_encode(bytes(PRIVATE_KEY.getPublicKey().toBytes()), "base58btc")

PUBLIC_KEY_DER_2 = multibase_encode(bytes(PRIVATE_KEY_2.getPublicKey().toBytes()), "base58btc")

IDENTIFIER = f"did:hedera:{NETWORK}:{PUBLIC_KEY_DER}_{DID_TOPIC_ID_1}"
IDENTIFIER_2 = f"did:hedera:testnet:{PUBLIC_KEY_DER_2}_{DID_TOPIC_ID_3}"

PRIVATE_KEY_ARR = [PrivateKey.generate() for _ in range(5)]

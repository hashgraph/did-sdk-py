from collections.abc import Callable

from hedera import Client, TopicId, TopicMessageSubmitTransaction, Transaction

from .hcs_message import HcsMessage
from .utils import execute_hcs_transaction_async


class HcsMessageTransaction:
    def __init__(
        self,
        topic_id: str,
        message: HcsMessage,
        transaction_builder: Callable[[TopicMessageSubmitTransaction], Transaction] | None = None,
    ):
        self.topic_id = topic_id
        self.message = message
        self._transaction_builder = transaction_builder

        self.executed = False

    async def execute(self, client: Client):
        if self.executed:
            raise Exception("This transaction has already been executed")

        if not self.message.is_valid(self.topic_id):
            raise Exception("HCS message is not valid")

        message_content = self.message.to_json()

        transaction = (
            TopicMessageSubmitTransaction().setTopicId(TopicId.fromString(self.topic_id)).setMessage(message_content)
        )

        if self._transaction_builder:
            transaction = self._transaction_builder(transaction)

        await execute_hcs_transaction_async(transaction, client)

        self.executed = True

from pydantic import BaseModel


class ChatSchema(BaseModel):
    id: str
    chat_name: str


class MessageFromSchema(BaseModel):
    id: str
    username: str


def load_message_from_schema(message_from: dict) -> MessageFromSchema:
    message_from_schema = MessageFromSchema(id=str(message_from['id']),
                                            username=message_from['username'])
    return message_from_schema


class MessageSchema(BaseModel):
    message_from: MessageFromSchema
    chat: ChatSchema
    text: str


def load_message_schema(message: dict) -> MessageSchema:
    message_from_schema = load_message_from_schema(message_from=message['from'])
    chat_name = message['chat'].get('title', None) or message['chat'].get('username', None)
    chat_schema = ChatSchema(id=str(message['chat']['id']),
                             chat_name=chat_name)
    message_schema = MessageSchema(message_from=message_from_schema,
                                   chat=chat_schema,
                                   text=message['text'])

    return message_schema


class CallbackSchema(BaseModel):
    callback_id: int
    message_from: MessageFromSchema
    message: MessageSchema
    data: str

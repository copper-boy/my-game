from pydantic import BaseModel


class ChatPrivateSchema(BaseModel):
    id: int
    first_name: str
    second_name: str
    username: str
    type: str = 'private'


class ChatSuperGroupSchema(BaseModel):
    id: int
    title: str
    type: str = 'supergroup'


class MessageFromSchema(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    second_name: str
    username: str


class MessagePrivateSchema(BaseModel):
    message_from: MessageFromSchema
    chat: ChatPrivateSchema
    date: int
    text: str


class MessageSuperGroupSchema(BaseModel):
    message_from: MessageFromSchema
    chat: ChatSuperGroupSchema
    date: int
    text: str

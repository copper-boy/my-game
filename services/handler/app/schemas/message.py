from pydantic import BaseModel


class ChatSuperGroupSchema(BaseModel):
    id: int
    title: str
    type: str = 'supergroup'


class MessageFromSchema(BaseModel):
    id: int
    username: str


class MessageSuperGroupSchema(BaseModel):
    message_id: int
    message_from: MessageFromSchema
    chat: ChatSuperGroupSchema
    text: str

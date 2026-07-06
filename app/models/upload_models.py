from pydantic import BaseModel


class UploadRequest(BaseModel):
    conversation_id: str
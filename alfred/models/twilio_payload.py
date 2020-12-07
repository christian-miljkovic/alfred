from pydantic import BaseModel, Field


class TwilioPayload(BaseModel):
    current_task: str = Field(None, alias="CurrentTask")
    current_input: str = Field(None, alias="CurrentInput")
    dialogue_sid: str = Field(None, alias="DialogueSid")
    memory: str = Field(None, alias="Memory")
    dialogue_payload_url: str = Field(None, alias="DialoguePayloadUrl")
    channel: str = Field(None, alias="Channel")
    next_best_task: str = Field(None, alias="NextBestTask")
    current_task_confidence: str = Field(None, alias="CurrentTaskConfidence")
    assistant_sid: str = Field(None, alias="AssistantSid")
    user_identifier: str = Field(None, alias="UserIdentifier")
    account_sid: str = Field(None, alias="AccountSid")

    def __str__(self):
        return "twilio_payload"

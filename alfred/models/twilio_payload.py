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
    user_phone_number: str = Field(None, alias="UserIdentifier")
    account_sid: str = Field(None, alias="AccountSid")

    def __str__(self):
        return f'''
            current_task: {self.current_task},
            current_input: {self.current_input},
            dialogue_sid: {self.dialogue_sid},
            memory: {self.memory},
            dialogue_payload_url: {self.dialogue_payload_url},
            channel: {self.channel},
            next_best_task: {self.next_best_task},
            current_task_confidence: {self.current_task_confidence},
            assistant_sid: {self.assistant_sid},
            user_phone_number: {self.user_phone_number},
            account_sid: {self.account_sid}
            '''

from pydantic import BaseModel, Field


class TwilioPayload(BaseModel):
    current_task: str
    current_input: str
    dialogue_sid: str
    memory: str
    dialogue_payload_url: str
    channel: str
    next_best_task: str
    current_task_confidence: str
    assistant_sid: str
    user_phone_number: str = Field(None, alias="user_identifier")
    account_sid: str

    def __str__(self):
        return f"""
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
            """

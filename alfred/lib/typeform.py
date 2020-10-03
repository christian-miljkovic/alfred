from alfred.models import Client, TypeformPayload
import datetime


def to_client(typeform_payload: TypeformPayload) -> Client:
    typeform_dict = typeform_payload.dict()
    answers = typeform_dict.get("form_response", {}).get("answers", None)
    client_data = {
        "first_name": None,
        "last_name": None,
        "phone_number": None,
        "birthday": datetime.datetime.now(),
    }
    for answer in answers:
        attribute = answer.get("field", {}).get("ref", None)
        if attribute == "phone_number":
            client_data["phone_number"] = answer.get("phone_number")
        else:
            client_data[attribute] = answer.get("text")

    return Client(**client_data)
from alfred.core.config import REACT_APP_URL

BIRTHDAY_REMINDER_MESSAGE = (
    lambda friend_list: f"It's {', '.join(friend_list)} birthday today! Don't forget to send them some love today!"
)

FAILURE_MESSAGE = (
    "Sorry, something went wrong on my end. Text +12035724630 to have this issue resolved immediately thank you!"
)

SHOW_BIRTHDAY_FORM_MESSAGE = (
    lambda client_id, first_name, last_name: f"{first_name} wants to save a reminder for your birthday! Please follow this link: {REACT_APP_URL}/birthday/{client_id} and fill in the date so that we can send you birthday messages! - Sent on behalf of {first_name} {last_name} by Alfred their personal assistant"
)

SHOW_FRIENDS_TABLE_MESSAGE = (
    lambda client_id: f"Here's the link {REACT_APP_URL}/table/{client_id} let me know if you need anything else!"
)

SUCCESS_BIRTHDAY_GATHER_MESSAGE = "Just sent to everyone! Now sit back and let me handle all of it :)"

NEW_CLIENT_WELCOME_MESSSAGE = "Hi, let's get started with getting to know each other. It'll be easier from here: https://christianmmiljkovic.typeform.com/to/TRTx7YTG"

RETURNING_CLIENT_WELCOME_MESSSAGE = "Hey! Hope you're having a great day! How can I help you?"

REDIRECT_TO_FRIENDS_TABLE_MESSAGE = (
    lambda client_id: f"Head on over to {REACT_APP_URL}/table/{client_id} to add some friends birthdays! You can now just say 'show my friends' to get the link to your friends table!"
)

RECOMMENDATION_MESSAGE = "Thanks for your recommendation, I'll be sure to start cookin' on that!"

SUCCESSFUL_SIGN_UP = (
    "That was awesome meeting you! From now on I am your trusted assistant who you can ask for anything!"
)

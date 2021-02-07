from alfred.core.config import REACT_APP_URL

BIRTHDAY_REMINDER_MESSAGE = (
    lambda friend_list: f"It's {', '.join(friend_list)} birthday today! Don't forget to send them some love today!"
)

FAILURE_MESSAGE = (
    "Sorry, something went wrong on my end. Text +12035724630 to have this issue resolved immediately thank you!"
)

SHOW_BIRTHDAY_FORM_MESSAGE = (
    lambda client_id, friend_id, client_first_name, client_last_name, friend_first_name: f"Hey {friend_first_name}! {client_first_name} wants to make a reminder for your birthday! Please follow this link: {REACT_APP_URL}/{client_id}/friend/form/{friend_id} to fill in your info! - Sent on behalf of {client_first_name} {client_last_name} by Alfred their personal assistant. More info at http://alfred-penny.com"
)

SHOW_FRIENDS_TABLE_MESSAGE = (
    lambda client_id: f"Here's the link {REACT_APP_URL}/table/{client_id} let me know if you need anything else!"
)

SUCCESS_BIRTHDAY_GATHER_MESSAGE = "Now sit back and let me handle all of it :)"

NEW_CLIENT_WELCOME_MESSSAGE = "Hi, let's get started with getting to know each other. It'll be easier if you put your info in here: https://christianmmiljkovic.typeform.com/to/TRTx7YTG also to see what I can do just say 'what can you do'"

RETURNING_CLIENT_WELCOME_MESSSAGE = (lambda client_first_name: f"Hey {client_first_name}! Hope you're having a great day! How can I help you? You can also say 'what can you do' to find out more!")

REDIRECT_TO_FRIENDS_TABLE_MESSAGE = (
    lambda client_id: f"Head on over to {REACT_APP_URL}/table/{client_id} to add some friends to your contacts list! You can now just say 'show my friends' to get the link to your contact list!"
)

RECOMMENDATION_MESSAGE = "Thanks for your recommendation, I'll be sure to start cookin' on that!"

SUCCESSFUL_SIGN_UP = (
    "That was awesome meeting you! From now on I am your trusted assistant who you can ask for anything!"
)

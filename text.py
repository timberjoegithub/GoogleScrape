"""
    Sends a text message to a phone number through the specified carrier.

    Args:
        phone_number_inside (str): The phone number to send the message to.
        carrier_inside (str): The carrier of the phone number.
        message_inside (str): The message content to be sent.

    Returns:
        None
    """
import smtplib
import sys

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}

EMAIL = "EMAIL"
PASSWORD = "PASSWORD"

def send_message(phone_number_inside, carrier_inside, message_inside):
    """
    Sends a text message to a phone number through the specified carrier.

    Args:
        phone_number_inside (str): The phone number to send the message to.
        carrier_inside (str): The carrier of the phone number.
        message_inside (str): The message content to be sent.

    Returns:
        None
    """
    recipient = phone_number_inside + CARRIERS[carrier_inside]
    auth = (EMAIL, PASSWORD)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
    server.sendmail(auth[0], recipient, message_inside)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: python3 {sys.argv[0]} <PHONE_NUMBER> <CARRIER> <MESSAGE>")
        sys.exit(0)
    phone_number = sys.argv[1]
    carrier = sys.argv[2]
    message = sys.argv[3]
    send_message(phone_number, carrier, message)

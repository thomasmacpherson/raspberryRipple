"""Example Pi Passport program."""
import pipassport
import time


API_KEY = 'abcd1234'


if __name__ == '__main__':
    while True:
        print("Swipe a card to post a transaction for that user.")
        cardid = pipassport.get_card_id()

        userinfo = pipassport.request_user_info(API_KEY, cardid)
        if not pipassport.card_valid(userinfo):
            print("Invalid card!")
            break
        else:
            pipassport.post_transaction(API_KEY, cardid, 'I did a thing!')
            print("Sent transaction for {} {}".format(userinfo['first_name'],
                                                      userinfo['last_name']))
            time.sleep(2)

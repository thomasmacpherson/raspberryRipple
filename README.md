Pi Passport API -- Python Client
================================

Pi Passport stores data associated with a user and some 'event' -- so it might be attendance at a Raspberry Pi event, a link to a photo taken, or a score  from playing a game.

The library communicates with the Pi Passport website and allows you to create transactions using an NFC card reader.

You can later retrieve and query this data over the web and as json.

The library relies on nxppy https://github.com/svvitale/nxppy to talk to http://www.nxp.com/demoboard/PNEV512R.html

Check `example.py` to see how to integrate this with your application.

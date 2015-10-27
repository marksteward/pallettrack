#!/usr/bin/env python
import json
from pallettrack import get_order, order_url
import os
import socket
import re

pallets = [
#    ('184256-793', '/home/ms7821/git/pallettrack/clubmate.json'),
#    ('189734-10058', '/home/ms7821/git/pallettrack/ccc2015out.json'),
#    ('190821-10058', '/home/ms7821/git/pallettrack/ccc2015return.json'),
    ('204937-793', '/home/ms7821/git/pallettrack/clubmate2.json')
]

def announce(message):
    print 'Sending %s' % message
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(('irccat', 12345))
        s.send('#london-hack-space %s' % message)
        s.close()
    except Exception, e:
        print e


def check_pallet(tracking_number, path):
    if os.path.exists(path):
        with open(path) as f:
            old_order = json.load(f)
    else:
        old_order = {}

    new_order = get_order(tracking_number)
    
    if old_order:
        updates = []
        if new_order['from'] != old_order['from']:
            updates.append('Collection address changed to "%s"' % (new_order['from'].replace('\n', ', ')))

        if new_order['to'] != old_order['to']:
            updates.append('Delivery address changed to "%s"' % (new_order['to'].replace('\n', ', ')))

        history_updates = []
        for h in reversed(new_order['history']):
            if h not in old_order['history']:
                h_msg = h['Comments']
                h_msg = re.sub('\s+', ' ', h_msg)
                history_updates.append(h_msg)


        updates += history_updates

        if updates:
            #print 'Announcing updates to %s' % tracking_number
            if len(updates) <= 3:
                announce('Pallet %s updates:' % tracking_number)
            else:
                announce('Pallet %s last 3 updates (more at %s):' % (tracking_number, order_url + tracking_number))

            for u in updates[:3]:
                announce('  %s' % u)


    with open(path, 'w') as f:
        json.dump(new_order, f)

for tracking_number, path in pallets:
    check_pallet(tracking_number, path)


#!/usr/bin/env python
import requests
from lxml import html, etree
from copy import deepcopy
from pprint import pprint

order_url = 'http://www.nationalpallets.co.uk/trackorder.aspx?trackingnumber='

def text_br(el):
    el = deepcopy(el)
    for line in el.xpath('//br'):
        if line.tail:
            line.tail = '\n' + line.tail
    return el.text_content()

def get_order(tracking_number):
    resp = requests.get(order_url + tracking_number)

    body = html.fromstring(resp.content)
    wrapper = body.cssselect('#wrapper')[0]

    summary = wrapper.cssselect('h1')[0].text_content()

    from_address = text_br(wrapper.cssselect('h2:contains("Collection Address") + p')[0])
    to_address = text_br(wrapper.cssselect('h2:contains("Delivery Address") + p')[0])

    tables = wrapper.cssselect('table')
    if not tables:
        histrows = []
    else:
        history = tables[0]
        columns = [th.text_content() for th in history.cssselect('thead th')]
        histrows = []
        for row in history.cssselect(':not(thead) > tr'):
            cells = [td.text_content().rstrip() for td in row.cssselect('td')]
            histrows.append(dict(zip(columns, cells)))

    order = {
        'summary': summary,
        'from': from_address,
        'to': to_address,
        'history': histrows,
    }
    return order



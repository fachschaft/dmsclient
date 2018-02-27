"""Drink Management System Client.

Usage:
  dms show (user|users|orders|products|events|comments)
  dms show sale [--days=<days>]
  dms (order|buy) <product>... [--number=<n>] [--user=<user>] [--force]
  dms comment <text>... [--user=<user>]
  dms setup completion
  dms (-h | --help)
  dms --version

Options:
  -h --help         Show this screen.
  --version         Show version.
  -u --user=<user>  (Partial) user's name. E.g. 'stef' for 'Stefan'
  -n --number=<n>   Number of bottles
  -f --force        Don't ask for confirmation
  --days=<days>     Number of days to show [default: 1].
"""
import os
import re
import configparser
from distutils.util import strtobool

from docopt import docopt
from tabulate import tabulate
from infi.docopt_completion.docopt_completion import docopt_completion

from dmsclient import DMSClient
from dmsclient import __version__


def print_users(users):
    table = ((user.first_name,
              user.last_name,
              "({})".format(user.user_name),
              user.allowed_buy)
             for user in users)
    print(tabulate(sorted(table), headers=['First Name', 'Last Name',
                                           'User Name', 'Allowed to Buy']))


def print_sale_entries(dms, sale_entries):
    table = ((se.date.strftime('%d.%m.%Y %H:%M'),
              se.product.name,
              se.profile.name)
             for se in sale_entries)
    print(tabulate(sorted(table, reverse=True), headers=['Date', 'Product', 'Profile']))


def print_products(products):
    def make_price(price):
        """ Sometimes the price is not set. Do not fail in this case but return
        Unknown
        """
        if price is None:
            return "Unknown"
        else:
            return "{:.2f}€".format(price/100)
    table = ((product.name, product.quantity,
              make_price(product.price_cent))
             for product in products)
    print(tabulate(sorted(table), headers=['Name', 'Quantity', 'Price']))


def print_comments(dms, comments):
    table = ((comment.profile.name, comment.comment)
             for comment in comments)
    print(tabulate(sorted(table), headers=['Profile', 'Text']))


def print_events(events):
    table = ((event.name, event.price_group, event.active)
             for event in events)
    print(tabulate(sorted(table), headers=['Name', 'Price Group', 'Active']))


def show(dms, args):
    if args['user']:
        print_users([dms.current_profile])
    elif args['users']:
        print_users(dms.profiles)
    elif args['orders']:
        print_sale_entries(dms, dms.orders)
    elif args['sale']:
        days = int(args['--days'])
        print_sale_entries(dms, dms.sale_history(days))
    elif args['products']:
        print_products(dms.products)
    elif args['comments']:
        print_comments(dms, dms.comments)
    elif args['events']:
        print_events(dms.events)
    else:
        raise NotImplementedError()


def search_interactive(query, choices):
    regex = re.compile(query.replace("*", ".*").replace(" ", ".*"),
                       re.IGNORECASE | re.DOTALL)
    choices = [(i, c) for i, c in enumerate(choices)
               if regex.search(c) is not None]
    if len(choices) > 5:
        print("Way too many like '{}' found.".format(query))
        exit(1)
    elif len(choices) > 1:
        for i, (ii, c) in enumerate(choices):
            print("({}) {}".format(i+1, c))
        choice_id = int(input("Please enter a number between 1 and {}: "
                              .format(len(choices)))) - 1
        if choice_id < 0 or choice_id >= len(choices):
            print("Selected nothing available, stupid.")
            exit(1)
        return choices[choice_id][0]
    elif len(choices) == 1:
        return choices[0][0]
    elif len(choices) == 0:
        print("Nothing like '{}' found.".format(query))
        exit(1)


def search_profile_interactive(dms, user_query):
    profiles = [u for u in dms.profiles if u.allowed_buy]
    user_names = ["{} {} {}".format(u.first_name, u.last_name, u.user_name)
                  for u in profiles]
    user_index = search_interactive(user_query, user_names)
    return profiles[user_index]


def select_yes_no(question, default_yes=True):
    if default_yes is None:
        question += ' [yes/no] '
    elif default_yes:
        question += ' [YES/no] '
    else:
        question += ' [yes/NO] '

    answer = input(question).strip().lower()
    if answer == '' and default_yes is not None:
        return default_yes
    try:
        return strtobool(answer)
    except ValueError as e:
        print("Only answer with yes or no.")
        exit(1)


def _general_sale(dms, args, upper_type, function):
    product_query = ' '.join(args['<product>'])
    products = [p for p in dms.products if p.quantity > 0]
    product_names = [p.name for p in products]
    product_index = search_interactive(product_query, product_names)
    product = products[product_index]

    user_query = args['--user']
    if user_query is not None:
        user = search_profile_interactive(dms, user_query)
        user_id = user.id
        user_name = user.name
    else:
        user_id = None

    if user_id is None or user_id == dms.current_profile.id:
        user_name = 'yourself'

    if args['--number'] is None:
        number = 1
    else:
        number = int(args['--number'])

    if (args['--force'] or
        select_yes_no('{} {} {} ({:.2f}€) for {}?'
                      .format(upper_type,
                              number,
                              product.name,
                              product.price_cent/100,
                              user_name))):
        for i in range(number):
            function(product.id, user_id)
        print("{} successful.".format(upper_type))
    else:
        print("Bye.")


def order(dms, args):
    _general_sale(dms, args, 'Order', dms.add_order)


def buy(dms, args):
    _general_sale(dms, args, 'Buy', dms.add_sale)


def comment(dms, args):
    text = ' '.join(args['<text>'])
    user_id = None
    user_query = args['--user']
    if user_query is not None:
        user_id = search_profile_interactive(dms, user_query).id
    dms.add_comment(text, user_id)
    print("Comment successful.")


def load_token():
    rcfile = os.path.expanduser('~/.dmsrc')
    token = None
    if os.path.isfile(rcfile):
        config = configparser.ConfigParser()
        config.read(rcfile)
        section = config['DEFAULT']
        if section:
            token = section['Token']

    if token:
        return token
    else:
        print('Expected token in file {} with content:'.format(rcfile))
        print('```\n[DEFAULT]\nToken = XxXXxxXXxXXxXX\n```')
        print('You can generate the token in the DMS account settings.')
        exit(1)


def main():
    args = docopt(__doc__, version='dmsclient {}'.format(__version__))
    token = load_token()
    api_endpoint = 'https://dms.fachschaft.tf/api'
    dms = DMSClient(token, api_endpoint)

    if args['show']:
        show(dms, args)
    elif args['order']:
        order(dms, args)
    elif args['buy']:
        buy(dms, args)
    elif args['comment']:
        comment(dms, args)
    elif args['setup'] and args['completion']:
        docopt_completion('dms')
        print('-> start a new shell to test completion')
    else:
        raise NotImplementedError()

if __name__ == "__main__":
    main()

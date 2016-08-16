import argparse
import imaplib
import sys

import time

import ptcaccount2
from ptcaccount2.mail import email_login, verify_email
from ptcaccount2.ptcexceptions import *


def parse_arguments(args):
    """Parse the command line arguments for the console commands.
    Args:
      args (List[str]): List of string arguments to be parsed.
    Returns:
      Namespace: Namespace with the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Pokemon Trainer Club Account Creator'
    )
    parser.add_argument(
        '-u', '--username', type=str, default=None,
        help='Username for the new account (defaults to random string).'
    )
    parser.add_argument(
        '-p', '--password', type=str, default=None,
        help='Password for the new account (defaults to random string).'
    )
    parser.add_argument(
        '-e', '--email', type=str, default=None,
        help='Email for the new account (defaults to random email-like string).'
    )
    parser.add_argument(
        '-b', '--birthday', type=str, default=None,
        help='Birthday for the new account. Must be YYYY-MM-DD. (defaults to a random birthday).'
    )
    parser.add_argument(
        '--compact', action='store_true',
        help='Compact the output to "username:password"'
    )
    parser.add_argument(
        '-n', '--number', type=int, default=1,
        help='Number of accounts to create'
    )
    parser.add_argument(
        '-s', '--mailserver', default=None,
        help='Number of accounts to create'
    )
    parser.add_argument(
        '-mp', '--mailpassword', default=None,
        help='Number of accounts to create'
    )

    return parser.parse_args(args)


def entry():
    """Main entry point for the package console commands"""
    args = parse_arguments(sys.argv[1:])
    if args.mailserver:
        M = imaplib.IMAP4_SSL(args.mailserver)
        email_login(M, args.email, args.mailpassword)

    for i in range(0, args.number):
        try:
            print("Creating new account:")
            account_info = ptcaccount2.random_account(args.username, args.password, args.email, args.birthday)
            if args.mailserver:
                while not verify_email(M):
                    print "activating email. Sleeping"
                    time.sleep(5)
            if args.compact:
                print('{}:{}'.format(account_info["username"], account_info["password"]))
            else:
                print('  Username:  {}'.format(account_info["username"]))
                print('  Password:  {}'.format(account_info["password"]))
                print('  Email   :  {}'.format(account_info["email"]))
                print('\n')
            with open("usernames.txt", "a") as ulist:
                ulist.write(account_info["username"]+":"+account_info["password"]+"\n")
                ulist.close()
            with open("supervisor.txt", "a") as ulist:
                ulist.write('-a "ptc" -u "%s" -p "%s"\n' % (account_info["username"], account_info["password"]))
                ulist.close()

        # Handle account creation failure exceptions
        except PTCInvalidPasswordException as err:
            print('Invalid password: {}'.format(err))
        except (PTCInvalidEmailException, PTCInvalidNameException) as err:
            print('Failed to create account! {}'.format(err))
        except PTCException as err:
            print('Failed to create account! General error:  {}'.format(err))

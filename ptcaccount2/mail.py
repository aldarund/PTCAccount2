import email
import email.header
import imaplib
import sys
from BeautifulSoup import BeautifulSoup
import  mechanize



def verify_email(M):
    print('Checking the mailbox.')
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Firefox')]

    # Sort through the emails for any from noreply@pokemon.com
    # Todo: Maybe make it a variable, so the script can be used for other stuff...?
    # ^ Probably not, the account creation is specific to the forms
    M.select('inbox')
    rv, data = M.search(None, '(FROM "noreply@pokemon.com")')
    if rv != 'OK' or data[0] == '' :
        print('No messages found!')
        return False

    # The main loop that gets the emails and activates them

    for num in data[0].split():

        # Attempts the fetch, and attempts again if an error is thrown
        # This previously would cause an error that stopped the script,
        # lets see if it can do it's bullshit this time when I a fuck
        # it with a while loop


        try:
            rv, data = M.fetch(num, 'RFC822')
        except:
            print('Fetch command failed, restarting the function')
            verify_email(M)
            break

        if rv != 'OK':
            print('Error getting message')
            return

        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0], 'utf-8')
        body = email.message_from_string(data[0][1])


        # IMAP doesn't give the entire email body in one go
        # So, we have to loop through the body if it is larger
        # than one part. Otherwise, it's one part and done

        if body.is_multipart():
            for payload in body.get_payload():

                # Beautiful soup filters out all the href links
                # inside the email bodies, and then I check if
                # the link contains the word "activated", which
                # is in all pokemon go activation links. Then I
                # delete the email.

                soup = BeautifulSoup(payload.get_payload())
                for link in soup.findAll('a'):
                    link = link.get('href')
                    if "activated" in link:

                        # Pretty sure this activates the link, could be fucked later on though
                        tried = 0
                        while tried < 5:
                            try:
                                print('Attempting to activate: %s' % tried)
                                br.open(link)
                                break
                            except:
                                tried += 1
                        print("%s", link)
                        M.store(num, '+FLAGS', '\\Deleted')
                        M.store(num, '+X-GM-LABELS', '\\Trash')
                        M.expunge()

        else:

            # Beautiful soup filters out all the href links
            # inside the email bodies, and then I check if
            # the link contains the word "activated", which
            # is in all pokemon go activation links. Then I
            # delete the email.

            soup = BeautifulSoup(body.get_payload())
            for link in soup.findAll('a'):
                link = link.get('href')
                if "activated" in link:

                    # Pretty sure this activates the link, could be fucked later on though
                    br.open(link)
                    tried = 0
                    while tried < 5:
                        try:
                            print('Attempting to activate: %s' % tried)
                            br.open(link)
                            break
                        except:
                            tried += 1
                    print("%s", link)
                    M.store(num, '+FLAGS', '\\Deleted')
                    M.expunge()
    return True
    print('Done checking emails')


def email_login(M, email, password):
    # Attempts a login with the data supplied in the header
    try:
        rv, data = M.login(email, password)
    except imaplib.IMAP4.error:
        print('Login failed!')
        sys.exit(1)

    # Selects the folder specified in the header
    rv, data = M.select('inbox')
    if rv == 'OK':
        print('Successful login')
        return True
    else:
        print("ERROR: Unable to open mailbox ", rv)
        return False

if __name__ == "__main__":
    M = imaplib.IMAP4_SSL("imap.gmail.com")
    email_login(M,'user','pwd')
    verify_email(M)
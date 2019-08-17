
from email.mime.text import MIMEText
import getpass  # if you want to use your username for sender
import smtplib


# Set the email parameters
# mail_from = getpass.getuser()
mail_from = 'username@example.com'
mail_to = 'username@example.com'


# Compose the message
message = '''<!DOCTYPE html> 
<html>
    <head> </head>
    <body>
        <table width="90%">
            <tr> 
                <td colspan="3"> <h1><center>Hello world</center></h1></td> 
            </tr>
            <tr>
                <td> <h2>Left</h1> </td>
                <td align="center"> <h2>Center</align></h2> </td>
                <td align="right"> <h2>Right</align></h2> </td>
            </tr>
        </table>
    </body> 
</html>
'''


# Create the message and envelope
envelope = MIMEText(_text=message, _subtype='html')
envelope['Subject'] = 'Here is my amazing HTML email'
envelope['To'] = mail_to
envelope['From'] = mail_from


# Send the mail
smtp = smtplib.SMTP()
smtp.connect(SERVER_NAME)
smtp.sendmail(envelope['From'], envelope['To'], envelope.as_string())
smtp.close()

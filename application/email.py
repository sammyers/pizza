from smtplib import SMTP
from constants import EMAIL_SERVER, EMAIL_USERNAME, EMAIL_PASSWORD

smtp = SMTP()
smtp.connect(EMAIL_SERVER)
smtp.ehlo()
smtp.starttls()
smtp.login(EMAIL_USERNAME, EMAIL_PASSWORD)

FROM = 'samuel.myers@students.olin.edu'
TO = 'sam@students.olin.edu'

message = """
From: Sam Myers <samuel.myers@students.olin.edu>
To: Sam Myers <sam@students.olin.edu>
Subject: Testing

This is a test for Consamables.
"""
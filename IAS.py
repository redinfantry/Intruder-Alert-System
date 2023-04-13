import smtplib
import datetime

# Set the threshold for failed login attempts
FAILED_ATTEMPTS_THRESHOLD = 5

# Set the email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_USERNAME = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_email_password'
ADMIN_EMAIL = 'admin_email@example.com'

# Set the log file path
LOG_FILE_PATH = '/var/log/auth.log'

# Define a function to send email notifications
def send_email(subject, message):
    try:
        # Create an SMTP client and initiate TLS connection
        smtp_client = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp_client.starttls()

        # Login to the email server
        smtp_client.login(EMAIL_USERNAME, EMAIL_PASSWORD)

        # Compose the email message
        email_message = f'Subject: {subject}\n\n{message}'

        # Send the email
        smtp_client.sendmail(EMAIL_USERNAME, ADMIN_EMAIL, email_message)

        # Close the SMTP connection
        smtp_client.quit()

        print('Email notification sent successfully.')
    except Exception as e:
        print(f'Error occurred while sending email notification: {str(e)}')

# Open the log file for reading
with open(LOG_FILE_PATH, 'r') as log_file:
    # Read the log file line by line
    for line in log_file:
        # Check if the line contains a failed login attempt
        if 'Failed password' in line:
            # Split the line into fields
            fields = line.strip().split()

            # Extract the username and IP address from the fields
            username = fields[8]
            ip_address = fields[10]

            # Print a message to the console
            print(f'Failed login attempt detected for {username} from {ip_address}.')

            # Send an email notification to the administrator
            message = f'Failed login attempt detected for {username} from {ip_address} at {datetime.datetime.now()}'
            send_email('Brute Force Attack Detected', message)

<p align="center" > <b> Birthday Reminder Application </b> </p>
The app runs as a Cron job daily and send emails to everyone from a given list of people, except the person who will be celebrating their birthday. The reminder email should be sent one week before
the person's birthday.

App usses microsoft outlook account (smtp-mail.outlook.com) to send emails, this coulbe changed in code by changing SMTP variable. 

# Table of contents

[//]: # (- [Birthday Reminder App]&#40;#birthday-reminder-app&#41;)

- [Table of contents](#table-of-contents)
- [Environment variables](#environment-variables)
- [Cron Job](#cron-job)


# Environment variables
To be able to send emails you need to define environment variables. To do this locally, create a .env file with two env variables:

```
LOGIN=youremail
PASSWORD=yourpassword
```
# Cron Job

To build cron job in terminal run:
``` 
>>> crontab -e
```
Crone setup:
``` 
>>> 0 9 * * * <path to app>/reminder.py <path to csv file> 1 (or 2 )
When third cron parameter is 1 app will verify contact file, when is set to 2 app will verify input, check if there is a contact who has birthday in a week, send emails if so.
``` 





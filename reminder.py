#! /usr/bin/python3

import csv
from datetime import datetime
import os
import smtplib
import sys
from dotenv import load_dotenv

load_dotenv()

SMTP = 'smtp-mail.outlook.com'
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')


def read_and_verify_contacts(contact_file_path: str):
    """
    Read  and verify contacts from csv file.
    :param contact_file_path: Path, as a string, to the csv file with all contacts
    :return: List of contacts and list of contacts with birthday in a week if file is valid.
    """
    with open(contact_file_path) as contacts_list:
        try:
            contacts = list(csv.reader(contacts_list))
        except csv.Error as e:
            return print(e)
    if not contacts:
        return print('File is empty')
    for contact in contacts:
        if len(contact) < 3 or any(value == '' for value in contact):
            return print('Some contact has missing values')
        try:
            date = datetime.strptime(contact[2][-5:], '%m-%d').date()
        except ValueError:
            return print(f'Incorrect birthday date for {contact[0]}!')
        if len(contact[2]) == 10:
            date = datetime.strptime(contact[2], '%Y-%m-%d').date()
            if date > datetime.today().date():
                return print(f'{contact[0]} is not born yet! Check the date of birth of this contact.')
    print('Contact file is valid')
    return contacts


def get_birthday_contacts(contacts):
    """
    Get contacts with birthday in a week
    :param contacts: List of contacts
    :return: List of contacts with birthday in a week
    """
    today = datetime.today().date()
    birthday_contacts = [contact for contact in contacts if (
            datetime.strptime(f'{today.year}-{contact[2][-5:]}', '%Y-%m-%d').date() - today).days == 7]
    return birthday_contacts


def build_email(name, name_of_birthday_person, date, amount_of_days):
    subject = "Subject: Birthday Reminder: %(name_of_birthday_person)s's birthday on %(date)s" % locals()
    email_text = "Hi %(name)s,\n" \
                 "This is a reminder that %(name_of_birthday_person)s will be celebrating their birthday on %(date)s.\n" \
                 "There are %(amount_of_days)s days left to get a present!" % locals()
    return subject, email_text


def send_email(email_address, subject, email):
    for i in range(3):
        try:
            with smtplib.SMTP(SMTP) as connection:
                connection.starttls()
                connection.login(user=LOGIN, password=PASSWORD)
                connection.sendmail(from_addr=LOGIN, to_addrs=email_address, msg=f'{subject}\n\n{email}')
                break
        except Exception:
            continue


def main(file_path, action):
    if not os.path.exists(file_path):
        return print('ERROR: File doesn\'t exist')
    if file_path.endswith('csv'):
        if action == '1':
            contacts = read_and_verify_contacts(file_path)
        elif action == '2':
            contacts = read_and_verify_contacts(file_path)
            if contacts:
                birthday_contacts = get_birthday_contacts(contacts)

                for contact in birthday_contacts:
                    email_list = contacts.copy()
                    email_list.remove(contact)
                    name_of_birthday_person = contact[0]
                    birthday_date = datetime.strptime(f'{datetime.today().year}-{contact[2][-5:]}', '%Y-%m-%d').date()
                    amount_of_days = (birthday_date - datetime.today().date()).days
                    for recipient in email_list:
                        name = recipient[0]
                        email_address = recipient[1]
                        subject, email = build_email(name, name_of_birthday_person, birthday_date, amount_of_days)
                        send_email(email_address, subject, email)
                print('Emails sent successfully')
    else:
        return print('ERROR: Wrong data format file')


if __name__ == '__main__':
    path_arg = sys.argv[1]
    action = sys.argv[2]

    main(path_arg, action)

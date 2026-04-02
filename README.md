# Address Book CLI Bot

## Project Overview
This project is a console-based assistant bot for managing an address book.

It allows users to store contacts, phone numbers, and birthdays, as well as view upcoming birthdays.

## Commands

- `hello` — Greet the bot  
- `add <name> <phone>` — Add a new contact or append a phone number  
- `change <name> <old_phone> <new_phone>` — Update an existing phone number  
- `phone <name>` — Show all phone numbers for a contact  
- `all` — Show all contacts  
- `add-birthday <name> <DD.MM.YYYY>` — Add birthday for a contact  
- `show-birthday <name>` — Show birthday of a contact  
- `birthdays` — Show upcoming birthdays within 7 days  
- `exit` / `close` — Save data and exit the program  

## Tech Stack
- Python
- OOP (Object-Oriented Programming)
- Dataclasses
- Pickle (data serialization)
- datetime
- Pipenv
- Docker


## Features

- Add and store contacts
- Add multiple phone numbers per contact
- Edit existing phone numbers
- Store and validate birthdays
- View all contacts
- Search for contact by name
- Show upcoming birthdays (next 7 days)
- Data serialization using file storage (pickle)

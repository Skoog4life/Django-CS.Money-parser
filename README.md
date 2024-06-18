# Django CS.Money Parser

## Overview
This project is a Django-based web application designed to parse data from the CS.Money website and Steam, comparing prices of CS skins and sending notifications if profitable trades are found.

## Features
- **Data Parsing:** Scrapes data from CS.Money and Steam.
- **Price Comparison:** Compares prices of skins on both platforms.
- **Profit Calculation:** Calculates profit percentage for each skin.
- **Notification System:** Sends notifications via Telegram if profit meets or exceeds a set threshold.
- **Admin Panel:** Utilizes Django for managing data and settings.
- **User Interaction:** Allows control through the console and Telegram bot.

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/Skoog4life/Django-CS.Money-parser.git
    cd Django-CS.Money-parser
    ```

2. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Create a .env file:**

    Create a `.env` file in the root directory of the project and add the following environment variables:

    ```sh
    TOKEN_API='YOU TOKEN_API'
    DJANGO_DEBUG=<True or False>
    SECRET_KEY='DJANGO SECRET_KEY'
    ```

    Replace the values with your actual data. Be sure to keep this file secure and do not commit it to your repository.

4. **Apply migrations:**

    ```sh
    python manage.py migrate
    ```

## Usage

1. **Start the Django server:**

    ```sh
    python manage.py runserver
    ```

2. **Run the Telegram bot:**

    ```sh
    python manage.py run_bot
    ```

3. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:8000/admin/`.

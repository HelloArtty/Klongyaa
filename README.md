# Klongyaa Senior Project

## Overview
Klongyaa is a senior project aimed at helping elderly people manage their medication schedules. The application provides reminders for taking pills, sends notifications via LINE, and allows caregivers to monitor the medication intake.

## Features
- **Pill Reminders**: Notify users when it's time to take their medication.
- **LINE Notifications**: Send notifications to caregivers if the user misses a dose.
- **Pill Management**: Add, edit, and delete pill information.
- **User-Friendly Interface**: Easy-to-use interface designed for elderly users.

## Installation

### Prerequisites
- Python 3.10
- PyQt5
- PyQt5designer
- pygame
- requests
- line-bot-sdk

### Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/HelloArtty/Klongyaa.git
    cd Klongyaa
    ```

2. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Run the main application:
    ```sh
    python main.py
    ```

2. Follow the on-screen instructions to navigate through the application.

## Project Structure
- `Klongyaa/`
  - `screen/`
    - `homeScreen/`
      - `main_homeScreen.py`: Main screen of the application.
      - `ui/`: Contains UI files for the home screen.
    - `inputPillNameScreen/`
      - `main_inputPillnameScreen.py`: Screen for inputting pill names.
      - `ui/`: Contains UI files for the input pill name screen.
    - `pillDetailScreen/`
      - `main_detail_screen.py`: Screen for displaying pill details.
      - `ui/`: Contains UI files for the pill detail screen.
    - `pillSummaryScreen/`
      - `main_summary_screen.py`: Screen for displaying pill summary.
      - `ui/`: Contains UI files for the pill summary screen.
    - `tutorialHomeScreen/`
      - `main_tutorial_screen.py`: Screen for displaying tutorial.
      - `ui/`: Contains UI files for the tutorial screen.
  - `shared/`
    - `data/`
      - `mock/`: Contains mock data for testing.
    - `images/`: Contains images used in the application.
  - `main.py`: Entry point of the application.
  - `requirements.txt`: List of required libraries.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.


## Acknowledgements
- PyQt5 for the GUI framework.
- LINE Bot SDK for the notification system.
- pygame for sound notifications.

## Contact
For any inquiries or issues, please contact [your email address].

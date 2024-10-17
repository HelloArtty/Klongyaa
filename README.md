# Klongyaa Senior Project

## Overview
Klongyaa is a project designed to help elderly people manage their medication schedules. The app provides reminders for taking pills, sends notifications via LINE, and allows caregivers to monitor medication intake.

## Features
- **Pill Reminders**: Notify users when it's time to take their medication.
- **LINE Notifications**: Send notifications to caregivers if the user misses a dose.
- **Pill Management**: Add and delete pill information.


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
    git clone https://github.com/yourusername/Klongyaa.git
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

- **Klongyaa/**: Main project folder
  - **screen/**: Contains files for different screens of the application
    - **homeScreen/**: 
      - `main_homeScreen.py`: Main screen showing the list of pills and options to view details or add new pills
    - **inputPillNameScreen/**: 
      - `main_inputPillnameScreen.py`: Screen for entering a new pill name
    - **pillDetailScreen/**: 
      - `main_detail_screen.py`: Displays pill details including name, dosage, and times to take
    - **pillSummaryScreen/**: 
      - `main_summary_screen.py`: Shows a summary of all pills the user needs to take
  - **shared/**: 
    - **data/**: Data used for testing
      - **mock/**: Mock data for testing
        - **config/**: Application configuration files
    - **images/**: Images used in the application
  - **ldrsensor/**: Folder for sensor-related files
  - **main.py**: Entry point of the application
  - **requirements.txt**: List of required libraries

## System Workflow

### Home Screen
- **File**: `main_homeScreen.py`
- **Description**: The main screen where users can see the list of pills they need to take. It also provides options to navigate to the pill detail screen or input new pill information.

### Pill Detail Screen
- **File**: `main_detail_screen.py`
- **Description**: Displays detailed information about a specific pill, including its name, dosage, and image. Users can edit or delete pill information from this screen.

### Pill Summary Screen
- **File**: `main_summary_screen.py`
- **Description**: Provides a summary of all the pills the user needs to take. Users can save the summary or edit the details of each pill.

### Input Pill Name Screen
- **File**: `main_inputPillnameScreen.py`
- **Description**: Allows users to input the name of a new pill. This screen is part of the process of adding a new pill to the system.

### Tutorial Screen
- **File**: `main_tutorial_screen.py`
- **Description**: Provides a tutorial for new users on how to use the application.

### Shared Components
- **Directory**: `shared/`
- **Description**: Contains shared resources such as images and mock data used across different screens.

## Notifications
- **LINE Notifications**: The application sends notifications via LINE to caregivers if the user misses a dose. This is handled using the `line-bot-sdk`.

## Sound Notifications
- **Sound Alerts**: The application uses `pygame` to play sound notifications when it's time to take a pill.

## Acknowledgements
- PyQt5 for the GUI framework.
- LINE Bot SDK for the notification system.
- pygame for sound notifications.

## Contact
For any inquiries or issues, please contact [your email address].
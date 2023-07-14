# Keylogger Readme

This Python program is a keylogger that captures and records keystrokes on a computer or mobile device. It also collects additional information such as system details, clipboard contents, captures screenshots, and records audio using the microphone. The captured data is then encrypted and sent via email to a specified address.

## Features
- Keystroke logging: Records all keystrokes made on the target device.
- System information: Collects information about the system, including hostname, IP addresses, processor, and operating system details.
- Clipboard monitoring: Captures and logs data copied to the clipboard.
- Microphone recording: Records audio for a specified duration using the device's microphone.
- Screenshot capture: Takes screenshots of the device's screen.
- Encryption: Encrypts the captured data using the Fernet encryption scheme.
- Email notification: Sends the encrypted data as email attachments to a specified email address.

## Requirements
- Python 3.x
- Required Python libraries: `email`, `socket`, `platform`, `win32clipboard`, `pynput`, `time`, `os`, `scipy`, `sounddevice`, `cryptography`, `getpass`, `requests`, `multiprocessing`, `PIL`, `smtplib`

## Installation and Usage
1. Clone or download the project files to your local machine.
2. Install the required Python libraries listed above using the pip package manager.
3. Update the email address and password variables in the code with your own email credentials.
4. Replace the `toaddr` variable with the email address where you want to receive the data.
5. Generate an encryption key using the Cryptography library and replace the `key` variable with your generated key.
6. Run the Python script to start the keylogger. The program will run in the background and silently record the data.
7. The captured data will be encrypted and sent via email according to the specified time intervals.
8. To stop the keylogger, press the `Esc` key or wait for the specified time duration to complete.

**Caution**: Please use this program responsibly and only on devices that you have proper authorization to monitor. Ensure that you comply with all applicable laws and regulations related to privacy and data protection.

## Disclaimer
The keylogger program provided here is for educational purposes only. The authors and contributors are not responsible for any misuse or damage caused by the use of this program. Use it at your own risk and discretion.

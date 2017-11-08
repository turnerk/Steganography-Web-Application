from PIL import Image
import re, math

message = "This is a test message to see if my monoalphabetic cipher is working properly"
password = "secret password"

def get_alphabet(password):
    # formats password to be processed
    password = password.lower()
    password = re.sub(r'[^a-z]', '', password)

    # unique_chars contains the order the cipher alphabet should go
    unique_chars = []
    for letter in password:
        if letter not in unique_chars:
            unique_chars.append(letter)
    for letter in range(97, 123, 1):
        if chr(letter) not in unique_chars:
            unique_chars.append(chr(letter))

    # alphabet contains the plain text to cipher text conversions
    alphabet = {}
    for letter in range(97, 123, 1):
        alphabet[chr(letter)] = unique_chars[letter-97].upper()

    return alphabet

def monoalphabetic_encode(message, password):
    # gets the cipher alphabet according to the password
    alphabet = get_alphabet(password)

    # ensures that the message is lower case
    message = message.lower()

    # replaces each plain text character with the corresponding cipher text character
    cipher_message = message
    for key, value in alphabet.items():
        cipher_message = cipher_message.replace(key, value)

    return cipher_message

def monoalphabetic_decode(cipher_message, password):
    # gets the cipher alphabet according to the password
    alphabet = get_alphabet(password)

    # ensures that the message is upper case
    cipher_message = cipher_message.upper()

    # replaces each cipher text character with the corresponding plain text character
    plain_message = cipher_message
    for key, value in alphabet.items():
        plain_message = plain_message.replace(value, key)

    return plain_message

def caesar_shift(message):
    # shift by 130 to make the text look not english
    new_message=['']*len(message)
    for i in range(0,len(message)):
        new_message[i] = chr(ord(message[i])+130)

    new_message = ''.join(new_message)
    return new_message

def start_location(password, x, y):
    # ROW
    # sum of ascii characters in the password
    sum_of_ascii_chars=0
    for char in password:
        sum_of_ascii_chars+=ord(char)

    # find the ascii value of the middle characters
    # even
    if len(password) % 2 == 0:
        middle = int(len(password)/2)
        middle = int((ord(password[middle-1]) + ord(password[middle]))/2)
    # odd
    else:
        middle = ord(password[math.ceil(len(password)/2)-1])

    row_start = (sum_of_ascii_chars * middle) % x
    print(row_start)

    # COLUMN
    # finds the number of unique characters in the password
    unique_chars = []
    for letter in password:
        if letter not in unique_chars:
            unique_chars.append(letter)

    # gets the first alphabetic character in the password
    alphabetic = ''.join([c for c in sorted(unique_chars) if ord(c)>=65])

    column_start = (len(password) * len(unique_chars) * ord(alphabetic[0])) % y
    print(column_start)

print("ENCODED:")
enciphered = monoalphabetic_encode(message, password)
print(enciphered)
print("DECODED:")
print(monoalphabetic_decode(enciphered, password))
print(caesar_shift(enciphered))

# open the image to read from
image_path = "test.png"
img = Image.open(image_path)
# retreives size of the image
(x, y) = img.size
start_location(password, x, y)

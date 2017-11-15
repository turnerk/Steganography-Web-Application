from PIL import Image
import re, math

X_BITS = 2
COLOR = 'red'

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

def caesar_shift(message, method):
    # shift by 13 to make the text look not english
    new_message=['']*len(message)
    for i in range(0,len(message)):
        if method=='encode':
            new_message[i] = chr(ord(message[i])-13)
        elif method=='decode':
            new_message[i] = chr(ord(message[i])+13)
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

    # COLUMN
    # finds the number of unique characters in the password
    unique_chars = []
    for letter in password:
        if letter not in unique_chars:
            unique_chars.append(letter)

    # gets the first alphabetic character in the password
    alphabetic = ''.join([c for c in sorted(unique_chars) if ord(c)>=65])

    column_start = (len(password) * len(unique_chars) * ord(alphabetic[0])) % y
    return(row_start, column_start)

# open the image to read from
image_path = "test1.png"#"test1.png"
img = Image.open(image_path)

#password = "My secret password"
password = None

# message_string will contain the final message
message_string = ""

# loads image
pix = img.load()

if len(img.getbands())==3:
    channels='RGB'
elif len(img.getbands())==4:
    channels='RGBA'

# retreives the size of the image and loops through each pixel of the image
(x, y) = img.size

# char_string will hold 8 bits to be converted to a character
char_string=""

# gets the location in the image to start decoding
if password:
    i, j = start_location(password, x, y)
else:
    i, j = 0,0

orig_i = i
orig_j = j
# loops through each pixel until a NULL character is found
counter = 0
eom_found = False
while True:
    if channels=='RGBA':
        # gets RGBA value of the pixel
        (red, green, blue, alpha) = pix[i, j]
    elif channels=='RGB':
        # gets RGB value of the pixel
        (red, green, blue) = pix[i, j]

    # add the last two bits of the COLOR value to char_string
    if COLOR == 'red':
        char_string+=(("{0:0%db}" % X_BITS).format(red & ((2**X_BITS)-1)))
    elif COLOR == 'green':
        char_string+=(("{0:0%db}" % X_BITS).format(green & ((2**X_BITS)-1)))
    elif COLOR == 'blue':
        char_string+=(("{0:0%db}" % X_BITS).format(blue & ((2**X_BITS)-1)))

    # once char_string is 8 bits long it gets converted to a character and added to message_string
    if len(char_string)>=8:
        byte_string = char_string[0:8]
        char_int = int(byte_string, 2)
        message_string+=(chr(char_int))
        char_string=char_string[8:]

        # break if a NULL byte is found
        if (char_int) is 0:
            eom_found = True
            break

    # increments the column, if at the end of the column goes back to 0 and increments the row.  If at the end of columns and rows goes back to the beginning
    i+=1
    if i == x:
        i = 0
        j+=1
        if j == y:
            j=0

    if i == orig_i and j == orig_j:
        print("looped through whole image")
        break

# print the message found in the image
if eom_found == True:
    print("DECODED:")
    if password:
        unshifted = caesar_shift(message_string, 'decode')
        message_string = monoalphabetic_decode(unshifted, password)
    print(message_string)
else:
    print("No message found")
# close the image
#Image.close("test1.png")

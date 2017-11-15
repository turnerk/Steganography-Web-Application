from bitarray import bitarray
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

# given a password and the size of the image, a "random" place in the image to start encoding is returned
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
    return (row_start, column_start)

# takes in a bit array and returns the X left most bits and the bit array without those bits
# if the bit array is empty then it returns 0 and the empty bit array
def get_next_x_bits(bit_array, bits):
    if len(bit_array)<bits:
        return (0, bit_array)
    X = bit_array[:bits]
    bit_array = bit_array[bits:]
    i = 0
    for bit in X:
        i = (i << 1) | bit
    return (i, bit_array)

message = "This is a test message.  A secret secret secret secret secret secret secret message.  Secretly.hkhdkhdgkashkhagk;hfdka;hgiera;nsdgk;adkhagjr;hiowehfadjhgbfajlhugireanvbsjkdsfathdlauramobleyhduihsdkjahguriealgugdfhuafilhjvzhbvubfiudhsfgriuqehvnuifkhdguriladhcnulkdxhfidlakshguriekdhbvnujgfbvb  aukfhuielqa huah h48ty89i4e hnudklhgnbfjaldbgukaghuithklfhdhigdhkjjk hgirhjgkahjkghuiralbnurialgbnujkhbgnrljhfrahagjjkdassuekfdknfi hehfkahuiaehgnhgnuirlhikjdhniek,dxzhioknfdiuxhkjnmfduihxjkguihszdxfghjikjkofadjhioshpgrioahiovfdhxckjgh8opaeihivhuierph opghuiphdaioklguirelkdcjmvjakehdgioherdnkj hg8oarephziofhieadhiugjverd joahrgkhnfjkneram8pdoxhgj84oiekdxhngva9e8iorlxeht8jo34wilshfnkjaerjdox8pf ;lgejrodicl gvpui;dhgjmv[o;xzh t8ogi[aelkdhxgnivodskxhgjkal;ngkdhsio'gieaszxfhioewahgireashfheiowadhgifoahjeriohigrhaezxigh4ioshb9eojahireab478iueugilgi5bj;giybht34wy89ary8]]a"
#password = "My secret password"
password = None

print("ENCODED:")
if password:
    enciphered = monoalphabetic_encode(message, password)
    shifted = caesar_shift(enciphered, 'encode')
    message = shifted
print(message)

#encode message to a bit array
encoded_message = message.encode()
ba = bitarray()
ba.frombytes(encoded_message)

#add a null byte to indicate the end of message
for i in range(8):
    ba.extend('0')

# open the image to read from
image_path = "Stegosaurus.png"
img = Image.open(image_path)

if len(img.getbands())==3:
    channels='RGB'
elif len(img.getbands())==4:
    channels='RGBA'

# loads image
pix = img.load()

# retreives size of the image
(x, y) = img.size

# calculates the maximum size of the message
max_message = ((x * y)/(8/X_BITS))-1
print("Your message should not exceed %d characters" % max_message)
print("Your current message is %d characters" % len(message))

# gets the location in the image to start encoding
if password:
    x_start, y_start = start_location(password, x, y)
else:
    x_start, y_start = 0,0

j = y_start
i = x_start

# loops through each pixel and modifies the COLOR bit to contain a portion of the message
while True:
    # gets the next x bits of the message
    (x_bits, ba) = get_next_x_bits(ba, X_BITS)

    if channels=='RGBA':
        # gets RGBA value of the pixel
        (red, green, blue, alpha) = pix[i, j]
    elif channels=='RGB':
        # gets RGB value of the pixel
        (red, green, blue) = pix[i, j]

    # makes the last x bits the x bits from the message
    # updates the pixel value
    if COLOR == 'red':
        red_aft = (red >> X_BITS << X_BITS) | x_bits
        pix[i, j] = (red_aft, green, blue)
    elif COLOR == 'green':
        green_aft = (green >> X_BITS << X_BITS) | x_bits
        pix[i, j] = (red, green_aft, blue)
    elif COLOR == 'blue':
        blue_aft = (blue >> X_BITS << X_BITS) | x_bits
        pix[i, j] = (red, green, blue_aft)

    if len(ba) == 0 and x_bits == 0:
        break

    # increments the column, if at the end of the column goes back to 0 and increments the row.  If at the end of columns and rows goes back to the beginning
    i+=1
    if i == x:
        i = 0
        j+=1
        if j == y:
            j=0


# saves the encoded image
img.save("test1.png")

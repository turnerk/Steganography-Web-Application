from bitarray import bitarray
from PIL import Image

# takes in a bit array and returns the two left most bits and the bit array without those bits
# if the bit array is empty then it returns 0 and the empty bit array
def get_next_two_bits(bit_array):
    if len(bit_array)<2:
        return (0, bit_array)
    two = bit_array[:2]
    bit_array = bit_array[2:]
    i = 0
    for bit in two:
        i = (i << 1) | bit
    return (i, bit_array)

message = "The novel opens with Mrs. Bennet trying to persuade Mr. Bennet to visit Mr. Bingley, an eligible bachelor who has arrived in the neighborhood. After some verbal sparring with Mr. Bennet baiting his wife, it transpires that this visit has already taken place at Netherfield, Mr. Bingley's rented house. The visit is followed by an invitation to a ball at the local assembly rooms that the whole neighbourhood will attend."

#encode message to a bit array
encoded_message = message.encode()
ba = bitarray()
ba.frombytes(encoded_message)

#add a null byte to indicate the end of message
for i in range(8):
    ba.extend('0')

# open the image to read from
image_path = "pup1.png"
img = Image.open(image_path)

# loads image
pix = img.load()

# retreives size of the image
(x, y) = img.size

# loops through each pixel and modifies the red bit to contain a portion of the message
for j in range(0, y):
    for i in range(0, x):
        # gets the next two bits of the message
        (two_bits, ba) = get_next_two_bits(ba)

        # gets RGB value of the pixel
        (red, green, blue) = pix[i, j]

        # makes the last two bits the two bits from the message
        red_aft = (red >> 2 << 2) | two_bits

        # updates the pixel value
        pix[i, j] = (red_aft, green, blue)

# saves the encoded image
img.save("test1.png")

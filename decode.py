from PIL import Image

X_BITS = 2
COLOR = 'blue'

# open the image to read from
image_path = "test1.png"

img = Image.open(image_path)

# message_string will contain the final message
message_string = ""

# loads image
pix = img.load()

# retreives the size of the image and loops through each pixel of the image
(x, y) = img.size

# char_string will hold 8 bits to be converted to a character
char_string=""

j = 0
i = 0
orig_i = i
orig_j = j
# loops through each pixel until a NULL character is found
eom_found = False
while True:
    # get RGB values for each pixel
    (red, green, blue) = pix[i,j]

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
    print(message_string)
else:
    print("No message found")
# close the image
#Image.close("test1.png")
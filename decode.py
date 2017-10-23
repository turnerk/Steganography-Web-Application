from PIL import Image

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

# loops through each pixel until a NULL character is found
for j in range(0, y):
    for i in range(0, x):
        # get RGB values for each pixel
        (red, green, blue) = pix[i,j]

        # add the last two bits of the red value to char_string
        char_string+=("{0:02b}".format(red & 3))

        # once char_string is 8 bits long it gets converted to a character and added to message_string
        if len(char_string)==8:
            message_string+=(chr(int(char_string, 2)))
            char_string=""

            # break if a NULL byte is found
            if int(char_string)==0:
                break

# print the message found in the image
print(message_string)

# close the image
Image.close("test1.png")

import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session
from werkzeug.utils import secure_filename
from werkzeug import SharedDataMiddleware
from flask_login import LoginManager
import string
import random
from bitarray import bitarray
from PIL import Image
import math, re
from math import ceil

#login_manager = LoginManager()

UPLOAD_FOLDER = os.path.basename('uploads')
ALLOWED_EXTENSIONS = set(['txt', 'png', 'wav'])

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
				 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
	'/uploads':  app.config['UPLOAD_FOLDER']
})
#login_manager.init_app(app)

@app.route('/getid')
def getid():
	session['username'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
	session['username'] = session['username'].replace(".","")
	session['message_string'] = 'No message found'
	return session['username']

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = getid() + ".png"# + secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#return redirect(url_for('uploaded_file',
									#filename=filename))
	path = getid()
	image_path = str("https://stega.me/uploads/" + path + ".png?t=")
	data = {}
	data['path_to_image'] = str(image_path)

	return render_template('index.html', data=data)

@app.route('/test')
def test():
	path = getid()
	image_path = str("uploads/" + path + ".png")
	img = Image.open(image_path)
	x, y = img.size
	return str(x)

@app.route('/encode', methods=['POST'])
def encode():
	message = request.form['messageToEncode']
	COLOR = request.form['colorSelect'].lower()
	password = ""
	password = str(request.form['optPwd']).strip()
	X_BITS = int(request.form['bitSlider'].strip())
	#encode message to a bit array
	encoded_message = message.encode()
	ba = bitarray()
	ba.frombytes(encoded_message)

	#add a null byte to indicate the end of message
	#for i in range(8):
		#ba.extend('0')

	# open the image to read from
	path = getid()
	image_path = str("uploads/" + path + ".png")

	img = Image.open(image_path)
	#img.save("uploads/" + path + ".png")

	#img = Image.open("uploads/" + path + ".png")
	channels='RGB'

	bands = len(img.getbands())
	if bands==4:
		channels='RGBA'
	# loads image
	pix = img.load()
	# retreives size of the image
	#(x, y) = (0, 0)
	(x, y) = img.size
	# calculates the maximum size of the message
	max_message = ((8/X_BITS) * x * y)-1
	#return str(max_message)
	# print("Your message should not exceed %d characters" % max_message)
	# print("Your current message is %d characters" % len(message))

	#gets the location in the image to start encoding
	if len(password) > 0:
		x_start, y_start = start_location(password, x, y)
		message = monoalphabetic_encode(message, password)
	else:
		x_start, y_start = 0,0

	j = y_start
	i = x_start
	# loops through each pixel and modifies the COLOR bit to contain a portion of the message
	(red, green, blue) = (0,0,0)
	(red, green, blue, alpha) = (0,0,0,0)
	while True:
		# gets the next x bits of the message
		(x_bits, ba) = get_next_x_bits(ba, X_BITS)

		# gets RGB value of the pixel

		if channels=='RGBA':
			(red, green, blue, alpha) = pix[i, j]
		else:
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
	img.save("uploads/" + path + "encoded.png")
	return redirect("uploads/" + path + "encoded.png")

# given a password and the size of the image, a "random" place in the image to start encoding is returned
def start_location(password, x, y):
	x = int(x)
	y = int(y)
	password = str(password)
	# ROW
	# sum of ascii characters in the password
	sum_of_ascii_chars=0
	for char in password:
		sum_of_ascii_chars+=ord(char)

	# find the ascii value of the middle characters
	# even
	middle = 0
	pwdlen = len(password)
	if (pwdlen % 2) == 0:
		middle = int(pwdlen/2)
		middle = int((ord(password[middle-1]) + ord(password[middle]))/2)
	# odd
	else:
		middle = int(pwdlen/2)
		middle = int(ceil(middle) - 1)
		middle = int(ord(password[middle]))
	

	row_start = (sum_of_ascii_chars * middle) % x

	# COLUMN
	# finds the number of unique characters in the password
	unique_chars = []
	for letter in password:
		if letter not in unique_chars:
			unique_chars.append(letter)

	# gets the first alphabetic character in the password
	alphabetic = ''.join([c for c in sorted(unique_chars) if ord(c)>=65])

	column_start = (pwdlen * len(unique_chars) * ord(alphabetic[0])) % y
	# print(row_start)
	# print(column_start)
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

@app.route('/decode', methods=['GET', 'POST'])
def decode():
	COLOR = request.form['colorSelectDe'].lower()
	password = ""
	password = str(request.form['optPwdDe']).strip()
	X_BITS = int(request.form['bitSliderDe'].strip())
	# open the image to read from
	image_path = "uploads/" + session['username'] + "encoded.png"

	img = Image.open(image_path)

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

	j = 0
	i = 0
	orig_i = i
	orig_j = j
	# loops through each pixel until a NULL character is found
	eom_found = False
	(red, green, blue) = (0,0,0)
	(red, green, blue, alpha) = (0,0,0,0)
	while True:
		# get RGB values for each pixel
		if channels=='RGBA':
			(red, green, blue, alpha) = pix[i, j]
		elif channels=='RGB':
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
			#return 'looped through whole image'
			break
	if len(password) > 0:
		message_string = str(message_string)
		message_string = monoalphabetic_decode(message_string, password)
	# print the message found in the image
	if eom_found == True:
		#return 'woot' + str(message_string)
		session['message_string'] = message_string
	else:
		session['message_string'] = 'No message found'
	return  session['message_string']

if __name__ == "__main__":
	app.run(debug=True)

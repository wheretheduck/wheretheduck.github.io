import urllib2
import urllib
import base64
import os

""""
def sendImage(path):
	page = 'http://18.221.191.217/upload.php'
	with open(path, "rb") as image_file:
		encoded_image = base64.b64encode(image_file.read())
	#print(encoded_image)
	raw_params = {'submit': 'true', 'upfile': encoded_image}
	#print(raw_params)
	params = urllib.urlencode(raw_params)
	print(params[0:20000])
	request = urllib2.Request(page, params)
	request.add_header("Content-type", "application/x-www-form-urlencoded; charset=UTF-8")
	page = urllib2.urlopen(request)
	info = page.info() 
	print(info)
	print(page.getcode())
	print(page.geturl())
"""

def sendImage(path):
	os.system("curl -F \"upfile=@"+os.path.abspath(path)+"\" http://18.221.191.217/upload.php")

if __name__ == "__main__":
	#test
	sendImage("/Users/dagan/Desktop/comics/up_here.png")
	sendImage("/Users/dagan/Desktop/comics/romance.jpg")
	sendImage("/Users/dagan/Desktop/comics/doctor_visit.png")

import urllib.request, json 
import sys
import subprocess

def error_window(msg : list[str]):
	import pygame as py
	from time import sleep
	py.init()
	py.font.init()
	font = py.font.Font(py.font.get_default_font(), 20)
	screen = py.display.set_mode((500,500), py.RESIZABLE)
	py.display.set_caption("ERROR")
	button = 0
	confirm = False
	while not confirm:
		for i in py.event.get():
			if i.type == py.QUIT:
				py.quit()
			if i.type == py.KEYDOWN:
				if i.key in [py.K_LEFT, py.K_q, py.K_a]:
					if button != 0:
						button = 0
				if i.key in [py.K_RIGHT, py.K_d]:
					if button != 1:
						button = 1
				if i.key == py.K_RETURN:
					confirm = True
		screen.fill((0,0,0))
		text = [font.render(i, 0, (255, 255, 255)) for i in msg]
		y = 50
		for i in text:
			w = screen.get_width()
			w2 = i.get_width()
			screen.blit(i, (w // 2 - w2 // 2, y))
			y += 50
		
		text = font.render("reessayer", 1, (255, 255, 255) if button !=1 else (255,0,0))
		screen.blit(text, (screen.get_width()//2 + text.get_width()//2, screen.get_height() - 50))
		text = font.render("jouer", 1, (255, 255, 255) if button !=0 else (255,0,0))
		screen.blit(text, (screen.get_width()//2 - 2*text.get_width(), screen.get_height() - 50))

		py.display.update()
		sleep(1/30)
	if confirm:
		if button == 0:
			subprocess.Popen([sys.executable, "./main.pyw"] + sys.argv[1:])
			py.quit()
		else:
			subprocess.Popen([sys.executable, "./updater.pyw"] + sys.argv[1:])
			py.quit()


		

try:
	import pygame
except:
	subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])

updates = {}
url = "https://asqel.github.io/updates.json"
ERROR = None
MESSAGES = {
	"404" : ["Une erreur s'est produite les information", "de mis a jour n'ont pas pu etre obtenue"],
	"Internet" : ["Une erreur de connetion s'est produite", "verrifier votre connetion"],
	"misc" : ["Une erreur inconnue s'est produite"]
}
try:
	response = urllib.request.urlopen(url)
except urllib.error.URLError as e:
	if str(e.reason) == "Not Found":
		ERROR = "404"
	else:
		ERROR = "Internet"
except Exception as e:
	ERROR = "misc"

if "" == ERROR:
	updates = json.load(response.read())
	print(updates)
else:
	message = MESSAGES[ERROR]
	error_window(message)	

	

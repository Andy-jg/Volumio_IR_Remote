#importing lirc and socketIO client
from socketIO_client import SocketIO, LoggingNamespace
import lirc

#Initiating
socketIO = SocketIO('localhost', 3000)
sockid = lirc.init("myprogram","/etc/lirc/lircrc")

def on_push_state(*args):
	global status
	status = args[0]['status'].encode('ascii', 'ignore')
	global artist
	artist = args[0]['artist'].encode('ascii', 'ignore')
	global title
	title = args[0]['title'].encode('ascii', 'ignore')
	global random
	random = 'random' in args[0]
	global seek
	seek = args[0]['seek']
	global duration
	duration = args[0]['duration']
	
socketIO.on('pushState', on_push_state)

# get initial state
socketIO.emit('getState', '', on_push_state)
socketIO.wait(seconds=0.1)

while True:
	button = lirc.nextcode()
	if len(button) <> 0:
		if button[0] == "Play":
			socketIO.emit('play')
		elif button[0] == "Pause":
			socketIO.emit('pause')
		elif button[0] == "Stop":
			socketIO.emit('stop')	
		elif button[0] == "Prev":
			socketIO.emit('previous')
		elif button[0] == "Next":
			socketIO.emit('next')
		elif button[0] == "Eject": #Playlist
			socketIO.emit('playPlaylist',{'name':'try'})
		elif button[0] == "Skip": #Random
			socketIO.emit('getState', '', on_push_state)
			socketIO.wait(seconds=0.1)
			print 'random'
			if random:
				socketIO.emit('setRandom','false')
				print 'setting random off'
			else:
				print 'setting random on'
				socketIO.emit('setRandom',{'value' : 'true'})
		elif button[0] == "For":
			socketIO.emit('getState', '', on_push_state)
			socketIO.wait(seconds=0.1)
			socketIO.emit('seek',seek/1000+10)
		elif button[0] == "Rev":
			socketIO.emit('getState', '', on_push_state)
			socketIO.wait(seconds=0.1)
			socketIO.emit('seek',max(seek/1000-10,0))
print "Good bye!"

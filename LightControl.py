import os
import colorsys
from flask import Flask
from flask import request
currcolor = '#000000'
swstatus = 0

app = Flask(__name__)

def hex2rgb(value):
	value = value.lstrip('#')
	length = len(value)
	return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))

def setColor(newcolor):
	global currcolor
	nr, ng, nb = hex2rgb(newcolor)
	pr, pg, pb = hex2rgb(currcolor)
	print('NEW COLOR = ' + newcolor)	
	cmd = 'sudo python3 /home/pi/light/raspiLight.py {} {} {} {} {} {} {}'.format(str(pr),str(pg),str(pb),str(nr),str(ng),str(nb),'15')
	os.system(cmd)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def test():
	return 'OK'

@app.route('/light')
def index():
	global swstatus, currcolor
	username = request.args.get('username')
	switch = request.args.get('switch')
	new_bri = request.args.get('bri')
	setcolor = request.args.get('color')
	if username == 'bioxakep':
		try:
			if switch == 'On':
				if swstatus == 0:
					setcolor = currcolor
					currcolor = '#000000'
					if setcolor != '#000000':
						setColor(setcolor)
						currcolor = setcolor
					else:
						setColor('#202020')
						currcolor = '#202020'
					print('ON')
					swstatus = 1
				else:
					print('ALREADY ON')
			elif switch == 'Off':
				if swstatus == 0:
					print('ALLREADY OFF')
				else:
					setColor('#000000')
					print('OFF')
					swstatus = 0
			elif switch == 'brightness' and int(new_bri) > 0:
				if swstatus == 0:
					currcolor = '#000000'
				channel = 255*(int(new_bri)/100)
				bri_color = '%02x%02x%02x' % (channel, channel, channel)
				bri_color = '#' + bri_color
				setColor(bri_color)
				currcolor = bri_color
				swstatus = 1
				print('SET BRI ' + str(new_bri) + '%')
			elif switch == 'color':
				if swstatus == 0:
					currcolor = '#000000'
				setColor(setcolor)
				currcolor = setcolor
				swstatus = 1
			else:
				print('error')				
		except Exception as e:
			print(e)
		return 'Light On\Off'
	else:
		return 'Unknown user'

@app.route('/state')
def state():
	global swstatus
	global currcolor
	statustype = request.args.get('type')
	if statustype == 'sw':
		return str(swstatus)
	elif statustype == 'bri':
		a, b, c = hex2rgb(currcolor)
		bri = (100*(a+b+c)) / (3*255)
		return str(bri)
	elif statustype == 'col':
		return str(currcolor.lstrip('#'))
	else:
		return 'ok'
		
if __name__ == '__main__':
	setColor('#000000')
	app.run(debug=False, host = '0.0.0.0', port=int('8484'))

from datetime import datetime
from flask import Flask, make_response, jsonify

# yeelight import––––––––––––––––––––––––––––––––––––––––––––
from yeelight import discover_bulbs
from yeelight import Bulb
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

app = Flask(__name__)

# for debugging purpose
# bulbs = [{'capabilities': {'bright': '50',
#                            'color_mode': '1',
#                            'ct': '2700',
#                            'fw_ver': '45',
#                            'hue': '359',
#                            'id': '0x0000000002dfb19a',
#                            'model': 'color',
#                            'name': 'bedroom',
#                            'power': 'off',
#                            'rgb': '16711935',
#                            'sat': '100',
#                            'support': 'get_prop set_default set_power toggle '
#                            'set_bright start_cf stop_cf set_scene cron_add '
#                            'cron_get cron_del set_ct_abx set_rgb set_hsv '
#                            'set_adjust set_music set_name'},
#           'ip': '192.168.0.19',
#           'port': 55443}]

# storing the discovered bulb here.
bulbs = []


def acting_period():
    now_time = datetime.now()
    # now_time = datetime(2018, 12, 31, 22, 23, 2, 686943)
    if now_time.hour >= 22 and now_time.hour <= 23 or now_time.hour >= 0 and now_time.hour <= 7:
        return True
    return False

# helper function - turn the light on and off ––––––––––––––––––––


def time_period():
    now_time = datetime.now()
    # now_time = datetime(2018, 12, 31, 22, 23, 2, 686943)
    if now_time.hour >= 22 and now_time.hour <= 23:
        return {'brightness': 80, 'color': '255,165,0'}
    elif (now_time.hour >= 0 and now_time.hour < 6):
        return {'brightness': 60, 'color': '255,0,0'}
    else:
        return {'brightness': 80, 'color': '0,0,255'}


def make_it_glow(ip_addr):
    character = time_period()
    # print('turn_it_on' + ip_addr)
    bulb = Bulb(ip_addr)
    bulb.turn_on()
    bulb.set_brightness(character.get('brightness'))
    color = character.get('color').split(',')
    bulb.set_rgb(int(color[0]), int(color[1]), int(color[2]))


def turn_it_off(ip_addr):
    # print('turn_it_off' + ip_addr)
    bulb = Bulb(ip_addr)
    bulb.turn_off()

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# routes –––––––––––––––––––––––––––––––––––––––––––––––––––––––––


@app.route("/turn_on")
def turn_on():
    global bulbs

    should_act = acting_period()

    # check if it's time to act or not
    if not should_act:
        return make_response(jsonify({'status': 'Not Now'}), 200)

    # check if there is  bulb in there
    if len(bulbs) < 0:
        bulbs = discover_bulbs()
        make_it_glow(bulbs[0].get('ip'))
    else:
        make_it_glow(bulbs[0].get('ip'))
    return make_response(jsonify({'status': 'Job Done'}), 200)


@app.route("/turn_off")
def turn_off():
    global bulbs

    should_act = acting_period()
    # check if it's time to act or not
    if not should_act:
        return make_response(jsonify({'status': 'Not Now'}), 200)

    # check if there is  bulb in there
    if len(bulbs) < 0:
        bulbs = discover_bulbs()
        turn_it_off(bulbs[0].get('ip'))
    else:
        turn_it_off(bulbs[0].get('ip'))
    return make_response(jsonify({'status': 'Job Done'}), 200)

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


if __name__ == '__main__':
    app.run()

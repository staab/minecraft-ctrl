import sys, re, time
from functools import lru_cache
from math import sin, cos
from time import sleep
from random import randint
from subprocess import run
from parse import parse_data


def die(message):
    print(message)
    sys.exit(1)


def get_stdout(command):
    return run(command, shell=True, capture_output=True).stdout.decode('utf-8')


def capture_pane(pane_id=None):
    return get_stdout(f"tmux capture-pane -t {pane_id or get_server_pane()} -p -S -10000")



@lru_cache()
def get_server_pane():
    for pane_id in get_stdout("tmux list-panes -F \#D").split('\n'):
        if '[Server thread/INFO]' in capture_pane(pane_id):
            return pane_id

    die("No minecraft server pane found.")


def find_line(pattern):
    lines = re.split(r'\[[\d:]+\] \[Server thread/INFO\]: ', capture_pane().replace('\n', ''))

    for line in reversed(lines):
        if pattern in line:
            return line


def send(command):
    run(f"tmux send-keys -t {get_server_pane()} '{command}{chr(10)}'", shell=True)


def get_data(target):
    send(f'/data get entity {target}')

    time.sleep(0.3)

    match_text = 'has the following entity data: '
    data = find_line(match_text).split(match_text)[1]

    return parse_data(data)


data = get_data('jstaab')
__import__("pprint").pprint({'position': data['Pos'], 'rotation': data['Rotation']})

def fill(x1, y1, z1, x2, y2, z2, block):
    send(f'/fill {x1} {y1} {z1} {x2} {y2} {z2} {block}')


def sphere(cx, cy, cz, radius):
    for i in range(36):
        x = sin(3.14 * (i / 36))
        y = cos(3.14 * (i / 36))

        print(x, y)

def block_city():
    for x in range(10):
        x_offset = randint(0, 20)
        y_offset = randint(0, 20)
        z_offset = randint(0, 20)

        cx = me[0] + x_offset
        cy = me[1] + y_offset
        cz = me[2] + z_offset

        fill(
            cx - 1,
            cy - 1,
            cz - 1,
            cx + 1,
            cy + 1,
            cz + 1,
            'water')


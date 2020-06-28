#!/usr/bin/env python3

from tkinter import Tk, StringVar, LEFT, BOTH, TOP, SUNKEN
from tkinter import ttk
import socket
import click
import signal

from elo import send_touch, send_move, send_release


@click.command()
@click.argument('host')
@click.argument('port', default=7777)
def main(host, port):
    '''HOST is the raspberry host ip to connect to and the PORT is the port to connect to, defaulted to 7777.'''

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    window = Tk()
    window.title('Elo Controller')
    window.config(padx=5, pady=5)
    window.geometry('800x600')

    pos_x = 200
    pos_y = 200
    window.geometry(f'+{pos_x}+{pos_y}')

    style = ttk.Style()
    style.configure('My.TFrame', background='#98fb98')

    top_frame = ttk.Frame(window, borderwidth=1, padding='3 3 3 3')
    top_frame.pack()

    max_x = 4095
    max_y = 4095

    elo_view = ttk.Frame(window, borderwidth=1, padding='3 3 3 3', style='My.TFrame')
    elo_view.config(relief=SUNKEN)
    elo_view.pack(side=TOP, fill=BOTH, expand=True)

    def get_elo_point(mouse_event):
        width = elo_view.winfo_width()
        height = elo_view.winfo_height()
        x = int(max_x * mouse_event.x / width)
        y = int(max_y * mouse_event.y / height)
        return x, y

    def tap_handler(event):
        x, y = get_elo_point(event)
        print(f'touch: ({x}, {y})')
        send_touch(sock, x, y)

    def mouse_b1_motion_handler(event):
        x, y = get_elo_point(event)
        send_move(sock, x, y)

    def mouse_b1_release_handler(event):
        x, y = get_elo_point(event)
        print(f'release: ({x}, {y})')
        send_release(sock, x, y)

    elo_view.bind('<Button-1>', tap_handler)
    elo_view.bind('<B1-Motion>', mouse_b1_motion_handler)
    elo_view.bind('<ButtonRelease-1>', mouse_b1_release_handler)

    sock = socket.socket()
    sock.connect((host, port))
    window.mainloop()


def signal_handler(signum, frame):
    print(f'Got signal {signum}')
    exit(0)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)


TOUCH = b'\x82'
MOVE = b'\x81'
RELEASE = b'\x84'
TAP_MOVE_COUNT = 10


class InvalidPacketTypeError(RuntimeError):
    pass


def lsb(val):
    return bytes([val & 0xff])


def msb(val):
    return bytes([val >> 8 & 0xff])


def packet(x, y, type):
    if type not in (TOUCH, MOVE, RELEASE):
        raise InvalidPacketTypeError('Invalid packet type specified')

    return b'T' + type + lsb(x) + msb(x) + lsb(y) + msb(y) + (b'\x20\x00' if type != RELEASE else b'\x00\x00')


def touch_packet(x, y):
    return packet(x, y, TOUCH)


def move_packet(x, y):
    return packet(x, y, MOVE)


def release_packet(x, y):
    return packet(x, y, RELEASE)


def send_tap(sock, x, y):
    send_touch(sock, x, y)
    for _ in range(TAP_MOVE_COUNT):
        send_move(sock, x, y)
    send_release(sock, x, y)


def send_touch(sock, x, y):
    sock.send(touch_packet(x, y))


def send_move(sock, x, y):
    sock.send(move_packet(x, y))


def send_release(sock, x, y):
    sock.send(release_packet(x, y))

import pytest
from unittest.mock import create_autospec, call

import socket

from elo import (TOUCH, MOVE, RELEASE, TAP_MOVE_COUNT, touch_packet,
                 move_packet, release_packet, lsb, msb, send_tap,
                 send_touch, send_move, send_release, InvalidPacketTypeError, packet)


x = 0x1234
y = 0xabcd
TOUCH_PACKET = b'T' + TOUCH + b'\x34\x12\xcd\xab\x20\x00'
MOVE_PACKET = b'T' + MOVE + b'\x34\x12\xcd\xab\x20\x00'
RELEASE_PACKET = b'T' + RELEASE + b'\x34\x12\xcd\xab\x00\x00'


@pytest.fixture
def f():
    class Fixture:
        sock_mock = create_autospec(socket.socket)
    return Fixture


def test_lsb():
    assert lsb(x) == b'\x34'


def test_msb():
    assert msb(x) == b'\x12'


def test_packet_must_raise_if_invalid_type_specified():
    with pytest.raises(InvalidPacketTypeError):
        packet(x, y, 0)


def test_packet_must_construct_correct_elo_report_packets():
    assert touch_packet(x, y) == TOUCH_PACKET
    assert move_packet(x, y) == MOVE_PACKET
    assert release_packet(x, y) == RELEASE_PACKET


def test_send_touch(f):
    send_touch(f.sock_mock, x, y)
    f.sock_mock.send.assert_called_with(TOUCH_PACKET)


def test_send_move(f):
    send_move(f.sock_mock, x, y)
    f.sock_mock.send.assert_called_with(MOVE_PACKET)


def test_send_release(f):
    send_release(f.sock_mock, x, y)
    f.sock_mock.send.assert_called_with(RELEASE_PACKET)


def test_send_tap_must_send_right_packet_sequence(f):
    send_tap(f.sock_mock, x, y)

    calls = [call.send(MOVE_PACKET) for _ in range(TAP_MOVE_COUNT)]
    calls.insert(0, call.send(TOUCH_PACKET))
    calls.append(call.send(RELEASE_PACKET))

    f.sock_mock.assert_has_calls(calls)


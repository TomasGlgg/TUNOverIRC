from pytun import TunTapDevice
from threading import Thread
from irc_client import IRC
from configparser import ConfigParser
from multipledispatch import dispatch
import base91


@dispatch(str)
def address_to_nick(addr):
    return bytes(map(int, addr.split('.'))).hex()


@dispatch(tuple)
def address_to_nick(addr):
    return bytes(addr).hex()


def get_src_dst(pkt):
    source = tuple(pkt[16:20])
    destination = tuple(pkt[20:24])
    return source, destination


def recv_irc_packet(message):
    print('Received:', message)
    pkt = base91.decode(message)
    tun.write(pkt)


def main():
    config = ConfigParser()
    config.read('config.conf')

    address = config['Interface']['address']
    netmask = config['Interface']['netmask']
    interface_name = config['Interface']['interface name']
    nick = config['IRC']['nick prefix'] + address_to_nick(address)
    host = config['IRC']['host']
    port = int(config['IRC']['port'])
    nick_prefix = config['IRC']['nick prefix']

    irc = IRC(host, port, nick)
    irc.connect_privmsg(recv_irc_packet)
    Thread(target=irc.process).start()

    mtu = int(400*(2-1.231))  # TODO

    global tun
    tun = TunTapDevice(interface_name)
    tun.mtu = mtu
    tun.addr = address
    tun.netmask = netmask
    tun.up()
    print('Interface up. Address: {}, netmask: {}, MTU: {}'.format(address, netmask, mtu))

    while True:
        pkt = tun.read(tun.mtu)
        source, destination = get_src_dst(pkt)
        destination_nick = nick_prefix + address_to_nick(destination)
        print('Destination: {}, destination nick: {}'.format(destination, destination_nick))
        message = base91.encode(pkt)
        irc.send(destination_nick, message)


if __name__ == '__main__':
    main()

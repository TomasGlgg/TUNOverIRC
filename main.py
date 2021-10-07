from pytun import TunTapDevice
from threading import Thread
from irc_client import IRC
from base64 import b85decode, b85encode

host = 'irc.libera.chat'
port = 6667
nick_prefix = 'TUNOIRC'
interface_name = 'TUI' + input('interface suffix>')
address = 0, int(input('last ip byte>'))
netmask = '255.255.0.0'
subnet = '10.8.'


def address_to_nick(addr):
    return bytes(addr).hex()


def get_src_dst(pkt):
    source = tuple(pkt[16:20])
    destination = tuple(pkt[20:24])
    return source, destination


def recv_irc_packet(message):
    print('Received:', message)
    pkt = b85decode(message)
    tun.write(pkt)


address_payload = '.'.join(map(str, address))   # 8.0.1
full_address = subnet + address_payload     # 10.8.0.1
nick = nick_prefix + address_to_nick(address)  # TUNOIRC080001
irc = IRC(host, port, nick)
irc.connect_privmsg(recv_irc_packet)
Thread(target=irc.process).start()

mtu = 100  # 468 - len(nick)
print(address, netmask)

tun = TunTapDevice(interface_name)
tun.mtu = mtu
tun.addr = full_address
tun.netmask = netmask
tun.up()

while True:
    pkt = tun.read(tun.mtu)
    source, destination = get_src_dst(pkt)  # 10.8.0.1 10.8.0.2
    print(source, destination)
    if not destination[0:2] == (10, 8):
        print('Not subnet')
        continue
    destination_nick = nick_prefix + address_to_nick(destination[2:])  # TUNOIRC0002
    print('Destination:', destination, destination_nick)
    message = b85encode(pkt).decode()
    print('Message:', message)
    irc.send(destination_nick, message)

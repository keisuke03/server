import socket
import urllib.parse

host_ip = input('please input host IPaddress')
host_port = int(input('please input host port'))

# ソケットを作成する
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
buffer_size = 1024
#minecraftのクライアントから送られるパケット 詳細は https://wiki.vg/Raknet_Protocol より
packet = b'\x01\x00\x00\x00\x00L\x00\x00\x00\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx\x00\x00\x00\x00\x00\x00\x00\x00'

print('connecting...')
sock.sendto(packet, (host_ip, host_port))
status, addr = sock.recvfrom(buffer_size)

if status[0:1] == b'\x1c':#packetIDが0x1c(Unconnected Pong)かどうか
#パケットで送られてくる形式が不明なので似ているURLデコードを使う \xを%に変えて疑似的に
    if str(status).split(';')[1] == '-1' or '':
        server_name = 'NONE'
    else:
        server_name = urllib.parse.unquote(str(status).split(';')[1].replace('\\x', '%'))
    server_protocol = str(status).split(';')[2]
    server_vertion = str(status).split(';')[3]
    server_connection_players = str(status).split(';')[4]
    server_max_players = str(status).split(';')[5]
    server_world_name = str(status).split(';')[7]
    server_gamemode = str(status).split(';')[8]
    if str(status).split(';')[10] == '-1' or '':
        server_port_ipv4 = 'NONE'
    else:
        server_port_ipv4 = str(status).split(';')[10]
    if str(status).split(';')[11] == '-1' or '':
        server_port_ipv6 = 'NONE'
    else:
        server_port_ipv6 = str(status).split(';')[11]

    print(f"server_name: {server_name}")
    print(f"server_protocol: {server_protocol}")
    print(f"server_vertion: {server_vertion}")
    print(f"server_connection_players: {server_connection_players}")
    print(f"server_max_players: {server_max_players}")
    print(f"server_world_name: {server_world_name}")
    print(f"server_gamemode: {server_gamemode}")
    print(f"server_port_ipv4: {server_port_ipv4}")
    print(f"server_port_ipv6: {server_port_ipv6}")

print('closing...')
sock.close()
input('please push any key...')
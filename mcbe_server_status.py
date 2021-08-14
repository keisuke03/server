import socket
import urllib.parse
import time

host_ip = input('please input host IPaddress')
host_port = int(input('please input host port'))
timeout_sec = 0.5#ping500msはtimeout判定

#新しく作るソケットのデフォルトのタイムアウト設定
socket.setdefaulttimeout(timeout_sec)
# ソケットを作成する
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
buffer_size = 5120
#minecraftのクライアントから送られるパケット 詳細は https://wiki.vg/Raknet_Protocol より
packet = b'\x01\x00\x00\x00\x00L\x00\x00\x00\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx\x00\x00\x00\x00\x00\x00\x00\x00'
out_error = ""
print('connecting...')
start_time = time.time()
sock.sendto(packet, (host_ip, host_port))
end_time = time.time()
status, addr = sock.recvfrom(buffer_size)
recv_time = time.time()
conn_time = (end_time - start_time) * 1000
recv_time = (recv_time - end_time) * 1000
total_time = conn_time + recv_time
if status[0:1] == b'\x1c':#packetIDが0x1c(Unconnected Pong)かどうか
#パケットで送られてくる形式が不明なので似ているURLデコードを使う \xを%に変えて疑似的に
    status = str(status).split('MCPE')[1]
    server_ip = addr[0]
    if status.split(';')[1] == '-1' or '':
        server_name = 'NONE'
    else:
        server_name = urllib.parse.unquote(status.split(';')[1].replace('\\x', '%'))
    server_protocol = status.split(';')[2]
    server_vertion = status.split(';')[3]
    server_connection_players = status.split(';')[4]
    server_max_players = status.split(';')[5]
    server_world_name = urllib.parse.unquote(status.split(';')[7].replace('\\x', '%'))
    try:
        server_gamemode = status.split(';')[8]
    except:
        server_gamemode = 'NONE'
    try:
        if status.split(';')[10] == '-1' or '':
            server_port_ipv4 = 'NONE'
        else:
            server_port_ipv4 = status.split(';')[10]
    except:
        server_port_ipv4 = 'NONE'
    try:
        if status.split(';')[11] == '-1' or '':
            server_port_ipv6 = 'NONE'
        else:
            server_port_ipv6 = status.split(';')[11]
    except:
        server_port_ipv6 = 'NONE'

    print(f"server_name: {server_name}")
    print(f"server_protocol: {server_protocol}")
    print(f"server_vertion: {server_vertion}")
    print(f"server_connection_players: {server_connection_players}")
    print(f"server_max_players: {server_max_players}")
    print(f"server_world_name: {server_world_name}")
    print(f"server_gamemode: {server_gamemode}")
    print(f"server_ip: {server_ip}")
    print(f"server_port_ipv4: {server_port_ipv4}")
    print(f"server_port_ipv6: {server_port_ipv6}")
    print(f"connection_time: {round(conn_time, 2)}ms")
    print(f"receive_time(ping): {round(recv_time, 2)}ms")
    print(f"total_time: {round(total_time, 2)}ms")


print('closing...')
sock.close()
input('please push any key...')
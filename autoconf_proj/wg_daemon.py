import os
import time

while True:
    if os.path.exists("client_public_key"):
        #get router pub key
        f = open("client_public_key")
        pub_key = f.read()
        pub_key = pub_key.strip()

        #get ip vpn tunnel
        f = open("ip")
        ip_wg = f.read()

        #get ip lan network on router
        f=open("ip_lan")
        ip_lan = f.read()
        peer = "[peer]"+"\n"+"PublicKey = "+pub_key+"\n"+"AllowedIPs = "+ip_wg+", "+ip_lan+"\n"
        f= open('wg0.conf', 'a')
        f.write(peer)
        f.close()
        #string = "wg set wg0 peer "+pub_key+" allowed-ips "+ip_wg+" allowed-ips "+ip_lan
        print (peer)
        os.system("wg-quick down wg0 && wg-quick up wg0")
        os.system("rm ip ip_lan client_public_key client_private_key")
    time.sleep(1)

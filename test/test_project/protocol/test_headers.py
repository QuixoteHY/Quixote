from quixote.protocol.headers import Headers


headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "HOST": "www.dongmengdai.com",
        "Referer": "https://www.dongmengdai.com/index.php?user&q=action/login",
}
# headers = {}

h = Headers(headers or {}, encoding='utf-8')

print(h)


h2 = h.get_aiohttp_headers()

print(h2)


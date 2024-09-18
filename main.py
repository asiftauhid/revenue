import requests, json


# cURL command coverted using https://www.scrapingbee.com/curl-converter/python/

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'multipart/form-data; boundary=---------------------------4071515539413151645828111389',
    'Origin': 'null',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Priority': 'u=0, i',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

data = '-----------------------------4071515539413151645828111389\r\nContent-Disposition: form-data; name="city"\r\n\r\nColombo\r\n-----------------------------4071515539413151645828111389\r\nContent-Disposition: form-data; name="av"\r\n\r\n1.0\r\n-----------------------------4071515539413151645828111389\r\nContent-Disposition: form-data; name="pt"\r\n\r\nWEBSITE\r\n-----------------------------4071515539413151645828111389\r\nContent-Disposition: form-data; name="did"\r\n\r\n6528612101718293506821\r\n-----------------------------4071515539413151645828111389\r\nContent-Disposition: form-data; name="userid"\r\n\r\n0\r\n-----------------------------4071515539413151645828111389\r\nContent-Disposition: form-data; name="dtmsource"\r\n\r\nnull\r\n-----------------------------4071515539413151645828111389\r\nContent-Disposition: form-data; name="srilanka"\r\n\r\nyes\r\n-----------------------------4071515539413151645828111389--\r\n'

response = requests.post('https://api2.pvrcinemas.com/PVRCinemasCMS/api/content/nowshowingnew2', headers=headers, data=data)

if(response.status_code == 200):
    nowShowingJSON = response.json()
    nowShowingMoviesJSON = nowShowingJSON['output']['mv']
    for key in nowShowingMoviesJSON:{ 
        print(key["n"]) 
}
        
import re
import requests

code_list = [['札幌市', '0110000'], ['仙台市', '0410001'], ['さいたま市', '1110000'], ['千葉市', '1210000'], ['柏市', '1221700'],
            ['千代田区', '1310100'], ['渋谷区', '1311300'], ['豊島区', '1311600'],  ['足立区', '1312100'], ['立川市', '1320200'],
            ['新潟市', '1510000'], ['名古屋市', '2310000'], ['京都市', '2610000'], ['大阪市', '2710000'], ['吹田市', '2720500'],
            ['神戸市', '2810000'], ['広島市', '3410000'], ['福岡市', '4013000'], ['うるま市', '4721300']]
output = {'text': ''}

for code in code_list:
    html = requests.get('https://www.jma.go.jp/jp/warn/f_' + code[1] + '.html').text
    data_list = re.findall('<span style="color:#FF2800">(.*?)</span>', html)

    if len(data_list) == 0:
        continue

    text = '【' + code[0] + '】'
    i = 1
    for data in data_list:
        if i == len(data_list):
            text += data
        else:
            data = re.sub('警報', '', data)
            text  += data + '，'
        i += 1
    output['text'] += text + '\n'

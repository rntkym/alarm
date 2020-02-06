from xml.etree import ElementTree
url_list = [requests.get('http://www.data.jma.go.jp/developer/xml/data/a73e24ea-4c1c-34f6-a678-e95381838662.xml'), # 北海道
        requests.get('http://www.data.jma.go.jp/developer/xml/data/5b4ef414-5987-3205-82d6-6bcdb00e6980.xml'), # 宮城
        requests.get('http://www.data.jma.go.jp/developer/xml/data/301fe470-1416-378e-9ad1-a5e26a079fab.xml'), # 埼玉
        requests.get('http://www.data.jma.go.jp/developer/xml/data/2089fbf8-0e12-39f9-84c9-8accfda24981.xml'), # 東京
        requests.get('http://www.data.jma.go.jp/developer/xml/data/17f743cb-4689-3f37-a030-7040c15cf2e4.xml'), # 千葉
        requests.get('http://www.data.jma.go.jp/developer/xml/data/365e1320-a4f0-3045-842a-f15be0a0d722.xml'), # 神奈川
        requests.get('http://www.data.jma.go.jp/developer/xml/data/a91940ab-cfbf-33c3-a3dd-6fd4cf13f99c.xml'), # 新潟
        requests.get('http://www.data.jma.go.jp/developer/xml/data/6a4c00de-6488-39fd-9146-aa2b9d1b4c1e.xml'), # 愛知
        requests.get('http://www.data.jma.go.jp/developer/xml/data/c83f420b-af59-30f8-b0e4-c1516fed319b.xml'), # 京都
        requests.get('http://www.data.jma.go.jp/developer/xml/data/520d4cc1-336e-306a-9892-323bc874b15f.xml'), # 大阪
        requests.get('http://www.data.jma.go.jp/developer/xml/data/97aa769f-e429-3399-a54d-f10f53096b4b.xml'), # 兵庫
        requests.get('http://www.data.jma.go.jp/developer/xml/data/f72558e4-3d10-3d79-be32-8f50131d4eb9.xml'), # 広島
        requests.get('http://www.data.jma.go.jp/developer/xml/data/dbdbf231-1fca-31b1-927e-978940215958.xml'), # 福岡
        requests.get('http://www.data.jma.go.jp/developer/xml/data/ba7d0282-0989-3aff-b206-f906564532c4.xml') # 沖縄
        ]
code_list = ['0110000', '0410001', '1110000', '1310100', '1311300', '1311300', '1311600', '1312100', '1320200','1210000',
            '1221700', '1410000', '1510000', '2310000', '2610000', '2710000', '2720500', '2810000', '3410000', '4013000', '4721300']
root_list = []
data = '{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}'
output = {'text': ''}

for url in url_list:
    url.encoding = 'utf-8'
    root_list.append(ElementTree.fromstring(url.text))

for root in root_list:
    for item in root.findall('./' + data + 'Body/' + data + 'Warning/' + data + 'Item'):
        code = item.find('./' + data + 'Area/' + data + 'Code')
        if code.text in code_list:
            area_name = item.find('./' + data + 'Area/' + data + 'Name')
            list = []
            for kind in item.findall('./' + data + 'Kind'):
                kind_text = ''
                kind_name = kind.find('./' + data + 'Name')
                if kind_name is None:
                    continue
                if not '警報' in kind_name.text:
                    continue
                kind_text += kind_name.text + '：'
                kind_status = kind.find('./' + data + 'Status')
                kind_text += kind_status.text
                list.append(kind_text)
            if not list:
                continue
            text = '【' + area_name.text + '】' + '、'.join(list)
            print(text)
            output['text'] = output['text'] + text + "\n"

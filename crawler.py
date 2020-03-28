import requests
from bs4 import BeautifulSoup
import json
import re

rootUrl = "https://www.takaratomy.co.jp/products/wixoss"
SearchUrl = rootUrl + "/card/card_list.php"
count = 0
CardInfo = {}
CardKind = {'ルリグ': 'LRIG',
            'アーツ': 'ARTS',
            'クラフト': 'CRAFT',
            'シグニ': 'SIGNI',
            'スペル': 'SPELL',
            'レゾナ': 'RESONA',
            'キー': 'KEY',
            'コイン': 'COIN'}
CardColor = {'白': 'white',
             '黒': 'black',
             '赤': 'red',
             '青': 'blue',
             '緑': 'green',
             '無': 'COLORLESS'}

post_form = {
    'search': '1',
    'keyword': '',
    'card_kind': '',
    'card_type': '',
    'rarelity': '',
    'support_formats[]': '1',
    'x': '81',
    'y': '30'
}
'''先通过条件找到最大搜索结果分页'''
session = requests.Session()
res = session.post(SearchUrl, data=post_form)
res.encoding = 'utf-8'
pageListSoup = BeautifulSoup(res.text, "html.parser")
pageList = pageListSoup.find(attrs="simple-pagination compact-theme").find_all('a')
maxPage = pageList[-1].string
'''从每个页面分类上获得单卡url'''
for i in range(1, int(maxPage) + 1):
    res = session.get(SearchUrl + '?card_page=' + str(i))
    res.encoding = 'utf-8'
    cardListSoup = BeautifulSoup(res.text, "html.parser")
    cardList = cardListSoup.find_all(class_='ajax cboxElement')
    pageCount = 0
    '''从单卡页面上获得卡面信息'''
    for card in cardList:
        if pageCount % 2 == 0:
            resCard = session.get(SearchUrl + card['href'])
            resCard.encoding = 'utf-8'
            cardSoup = BeautifulSoup(resCard.text, "html.parser")
            if cardSoup.td.string == 'コイン' or cardSoup.td.string == 'アーツ':
                continue
            cardInfo = dict()
            cardInfo['wxid'] = cardSoup.p.string
            cardInfo['name'] = cardSoup.h3.contents[0]
            rarity = cardSoup.find(class_='card_rarity txt_yellow').string
            cardInfo['rarity'] = re.sub('\W+', '', rarity)
            cardInfo['cardType'] = CardKind[cardSoup.td.string]
            other = cardSoup.find_all('td')
            cardColor = other[2].string
            finalColor = cardColor[0]
            if len(cardColor) > 1:
                for color in CardColor:
                    if color in other[2]:
                        finalColor = finalColor + '/' + CardColor[color]
            cardInfo['color'] = finalColor
            cardInfo['level'] = 0 if other[3].string == '-' else int(other[3].string)
            cardInfo['limit'] = 0 if other[6].string == '-' else int(other[6].string)
            cardInfo['power'] = 0 if other[7].string == '-' else int(other[7].string)
            cardInfo['limiting'] = other[8].string
            if cardSoup.td.string == 'ルリグ':
                cardInfo['coin'] = int(other[7].string)
            cardInfo['illust'] = cardSoup.find(class_='card_img').contents[3].split()[1]
            cardInfo['classes']
            cardInfo['costWhite']
            cardInfo['costBlack']
            cardInfo['costRed']
            cardInfo['costBlue']
            cardInfo['costGreen']
            cardInfo['costColorless']
            cardInfo['guardFlag']
            cardInfo['multiEner']
    pageCount += 1
    if i == 3:
        break

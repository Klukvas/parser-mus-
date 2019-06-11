import requests
from bs4 import BeautifulSoup
import re



def get_html(url):
    req = requests.get(url)
    return req.text

def getKey(dic):                                                                            #первое испольвание возвращает список из Жанра и сслыки на жанр
    linnkGanre = []                                                                         #второе использование возвражает название песни и сслылку на песню
    dicGanreInd = {}
    keys = dic.keys()
    print("Для выбора  введите соответствующее  число:", end="\n")
    for index, item in enumerate(keys):                 #enumerate - для индексирования
        print(f"{index} : {item}")
        dicGanreInd.update({index: item})
    userCho = input(":")
    try:
        ganre = dicGanreInd[int(userCho)]                       #получение названия песни по выбраному пользователем индексу
        linnkGanre.append(dicGanreInd[int(userCho)])            #добавление в список жанра/названия
        linnkGanre.append(dic.get(ganre))                  #добавление  в списоксслыки на жанр/ссылки на песню
    except:
        print(f"Вы ввели несуществующий индекс")
        exit(main())
    return linnkGanre

def getInfoSong(html):                                                                    #получение ссылки на скачивание, имени
    soup = BeautifulSoup(html, "html.parser")
    name = soup.find("div", class_="musicset-track-list__items")
    names = name.findAll('i', class_="musicset-player__icon")
    linkDown = name.findAll('div', class_ = "musicset-track__download track-geo")
    dic = {}
    for item, itemm in zip(names, linkDown):
        nameSong = item.get('title')
        nameSong = re.sub("Прослушать", ' ', nameSong)
        nameSong = nameSong.strip()
        linkk = itemm.find("a")
        linkk = linkk.get("href")
        linkk = "https://zaycev.net"+linkk
        dic.update({nameSong: linkk})

    return dic

def get_links(html):                                                                         #Получение всех ссылок на жанры
    nameLink = {}
    soup = BeautifulSoup(html, "html.parser")
    links = soup.findAll('li', class_='genre__filter-el')
    for item in links:
        try:
            link = item.find('a')
            link = link.get('href')
            link = "https://zaycev.net" + link
            name = item.text
            nameLink.update({name: link})


        except:
            continue
    return nameLink


def down(dic):
    nameLink = dic[1]
    re = requests.get(nameLink, stream=True)
    re = re.text
    soup = BeautifulSoup(re, "html.parser")
    linkToDonw = soup.find("div", class_="button button-download")
    linkToDonw = linkToDonw.find('a', id="audiotrack-download-link--dwnl")
    linkToDonw = linkToDonw.get("href")
    downw = requests.get(linkToDonw)
    print(r"Укажите абсолютный путь для скачивание песни(если оставить пустым - музыка будет скачана в актуальную папку скрипта) \n  Пример:  C:\Users\Andrew\Desktop\mus ") #C:\Users\Andrew\Desktop\mus
    way = input(":")
    if way == " " or way == "":
        with open(f"{dic[0]}.mp3", "wb") as file:
            file.write(downw.content)
        print("Музыка успешно загружена в актульную папку")
    else:
        try:
            way = way + "\\" + dic[0] + ".mp3"
            print(f"Местонахождение песни :  {way}")
            with open(f"{way}", "wb") as file:
                file.write(downw.content)
            print("Музыка успешно загружена в актульную папку")
        except:
            print("ошибка пути")

    return downw

def main():
    url = 'https://zaycev.net/genres/index.html'
    ganrMus = getKey(get_links(get_html(url)))
    redy = down(getKey(getInfoSong(get_html(ganrMus[1]))))

if __name__ == "__main__":
    main()


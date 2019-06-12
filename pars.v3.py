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
    nameSong = dic[0]
    if nameSong.strip() == "Скачать весь альбом":
        downw = requests.get(nameLink)
        print("Укажите абсолютный путь для скачивание песни(если оставить пустым - музыка будет скачана в актуальную папку скрипта)" + "\n" + r"Пример:  C:\Users\Andrew\Desktop\mus ")  # C:\Users\Andrew\Desktop\mus
        way = input(":")
        if way == " " or way == "":
            with open(f"{dic[0]}.zip", "wb") as file:
                file.write(downw.content)
            print("Музыка успешно загружена в актульную папку")
        else:
            try:
                way = way + "\\" + dic[0] + ".zip"
                print(f"Местонахождение песни :  {way}")
                with open(f"{way}", "wb") as file:
                    file.write(downw.content)
                print("Музыка успешно загружена в актульную папку")
            except:
                print("ошибка пути")
    else:
        re = requests.get(nameLink, stream=True)
        re = re.text
        soup = BeautifulSoup(re, "html.parser")
        linkToDonw = soup.find("div", class_="button button-download")
        linkToDonw = linkToDonw.find('a', id="audiotrack-download-link--dwnl")
        linkToDonw = linkToDonw.get("href")
        downw = requests.get(linkToDonw)
        print("Укажите абсолютный путь для скачивание песни(если оставить пустым - музыка будет скачана в актуальную папку скрипта)" +"\n"+  r"Пример:  C:\Users\Andrew\Desktop\mus ") #C:\Users\Andrew\Desktop\mus
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
#################################################################################################################################################
def getAllLinks(html):
    NameLinkAm = []
    soup = BeautifulSoup(html, "html.parser")
    all = soup.find("ul", class_="musicset-list unstyled-list clearfix")
    alllinks = all.findAll("li", class_="musicset-list__item")
    for item in alllinks:
        list = []
        content = item.find("meta")
        content = content.get("content")
        content = re.sub("– слушайте музыку онлайн или скачивайте треки без регистрации на zaycev.net", " ", content)
        content = content.strip()
        link = item.find("a", class_="musicset-item__pic-link")
        linkset = link.get("href")
        linkset = "https://zaycev.net" + linkset
        amount = item.find("div", class_='musicset-item__info')
        amount = amount.find("div", class_="musicset-item__details")
        amount = amount.find("p").text
        amount = amount.strip()
        list = [content,linkset,amount]
        NameLinkAm.append(list)
    print(NameLinkAm)
    print("Введите соответствующее число для выбора:")
    for index, item in enumerate(NameLinkAm):
        print(index,":", item[0])
    numb = int(input(":"))
    try:
        linkto = NameLinkAm[numb][1]
    except:
        print("Ошибка, несуществующий индекс")
        exit(main())
    return linkto

def getInfo(link):
    dic = {}
    html = get_html(link)
    soup = BeautifulSoup(html, "html.parser")
    downzip = soup.find("div", class_="musicset__buttons")
    downzip = downzip.find("a",class_="audiotrack-button__label track-geo__button")
    downzip = downzip.get("href")
    downzip = "https://zaycev.net" + downzip
    allAlb = "Скачать весь альбом"
    soup = soup.find("div", class_="musicset-track-list musicset-autoplayed")
    soup = soup.find("div", class_="musicset-track-list__items")
    soup = soup.findAll("div", class_="musicset-track clearfix")
    for item in soup:
        inf = item.find("div",class_="musicset-track__title track-geo__title")
        name = inf.find("i", class_="musicset-player__icon")
        name = name.get("title")
        name = re.sub("Прослушать", ' ', name)
        link = item.find("link")
        link = link.get("href")
        link = "https://zaycev.net"+link
        dic.update({name: link})
    dic.update({allAlb: downzip})
    return dic

def main():
    print("1:Выбрать песни по жанрам \n2: Выбрать музыкальные сеты")
    choo = int(input(":"))
    if choo == 1:
        url = 'https://zaycev.net/genres/index.html'
        ganrMus = getKey(get_links(get_html(url)))
        redy = down(getKey(getInfoSong(get_html(ganrMus[1]))))
    elif choo == 2:
        url = "https://zaycev.net/musicset/index.html"
        re = down(getKey(getInfo(getAllLinks(get_html(url)))))


if __name__ == "__main__":
    main()


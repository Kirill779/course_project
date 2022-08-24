import requests,json
import yadisk
from tqdm import tqdm
from tqdm import trange
from time import sleep
import pprint


vk_id = 739978517
vktoken = ''
token = ''

class MyVk:  # объявляем класс вк
    def __init__(self):
        self.token = ""
        self.id = 739978517
        self.likes = 0


    def get_photo_data(self):  # параметры для класса вк
        count = 5
        myapi = requests.get("https://api.vk.com/method/photos.get", params={
            'owner_id': vk_id,
            'access_token': vktoken,
            'album_id': 'profile',
            'count': count,
            'extended': 1,
            'photo_sizes': 0,
            'v': 5.103
        })
        return json.loads(myapi.text)

    def get_photos(self,NPh): # получаем фото
        data = self.get_photo_data()
        self.likes = (data['response']['items'][0]['likes']['count']) # выделяем лайки
        my_data = data['response']['items'][0]['sizes']
        photo = {}  # создаем два словаря - фото и фото на количество
        photo_NPh = {}
        count_photo = 0     # так же считаем общее количество фото
        print("Считаем фото")
        # используем прогресс-бар
        for url_photo in tqdm(my_data):
            sleep(0.3) #задержка в секундах
            photo[str(count_photo)] = url_photo['height'],url_photo['width'],url_photo['url'],url_photo['type']
            count_photo += 1
        print()
        i = 0
        if len(photo) <= NPh : # если фото меньше заданного, то забираем все фото
            photo_NPh = photo
        else:
            print("Выбираем фото")
            # используем прогресс-бар
            for i in trange(len(photo)):
                sleep(0.3)  # задержка в секундах
                if len(photo_NPh) < NPh :
                    photo_NPh[str(i)] = photo[str(i)]
                else:
                    for j in trange(len(photo_NPh)):  # если фото больше - начинаем выбирать нужные фото
                        sleep(0.3) #задержка в секундах
                        if photo[str(i)][0] > photo_NPh[str(j)][0]or (photo[str(i)][0] > photo_NPh[str(j)][0]and photo[str(i)][1] > photo_NPh[str(j)][1]):
                            if j < len(photo_NPh):
                                photo_NPh[str(j+1)] = photo_NPh[str(j)]
                            photo_NPh[str(j)] = photo[str(i)]
                            break

            i += 1
        return photo_NPh # возвращаем словарь фото


class YaUploader:   # объявляем класс яндекс диска
    def __init__(self, token: str):
        self.token = token
        self.url = ''
        self.param = {}
        self.heads = {}

    def get_headers(self,path_to_file,name_file):  # подбираем параметры, необходимые для записи на Ядиск
        self.heads = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        self.param = {'url':'','path':'', 'overwrite': 'true'}
        self.dirparam = {'path':path_to_file, 'overwrite': 'true'}
        return

    def mk_dir(self,file_path: str):  # создаем каталог на Ядиске (имя каталога не задано)
        mkurl = 'https://cloud-api.yandex.net/v1/disk/resources/'
        requests.put(url=mkurl, params=self.dirparam, headers=self.heads).json()


    def upload(self, path_file, photos,likes):  # записываем файлы на Ядиск
        file_for_json = []                    # собираем словарь для файла json
        i = 0
        print('\n',"Грузим фото в яднекс")
        # используем прогресс-бар
        for photo in tqdm(photos.values()):
            self.param['url'] = photo[2]
            file_for_json.append({'file_name': '', 'size': ''})
            path_disk = path_file + "/" + str(photo[0])  + str(likes) + '.'+'jpeg'
            file_for_json[i]['file_name'] += path_disk
            file_for_json[i]['size'] += photo[3]
            self.param['path'] = path_disk
            i += 1
            r = requests.post(url=self.url, params=self.param, headers=self.heads).json
        #записываем файл json
        with open("photos.json", "w") as file:
            json.dump(file_for_json, file, indent=3)

        return



if __name__ == '__main__':
    mevk = MyVk()
    Number_photo = 5
    vk_photo = mevk.get_photos(Number_photo)
    name_dir = 'vk_pic'
    token = ''
    uploader = YaUploader(token)
    uploader.heads
    uploader.get_headers(name_dir,vk_photo)
    path_file = uploader.mk_dir(name_dir)
    result = uploader.upload(name_dir,vk_photo,mevk.likes)
    print(result)

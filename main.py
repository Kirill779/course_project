import requests,json
import yadisk
from tqdm import tqdm
from tqdm import trange
from time import sleep
import pprint


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
        my_data = data['response']['items']
        # создаем два словаря - фото и фото на количество
        photo = {}
        photo_NPh = {}
        count_photo = 0     # так же считаем общее количество фото
        print("Считаем фото")
        print()
        # используем прогресс-бар
        for p in tqdm(my_data):
            sleep(1)
            #выбираем фото максимального размера
            max_photo = p['sizes'][0]
            for q in range(len(p['sizes'])):
                url_photo = p['sizes'][q]
                if url_photo['type'] == 'z':
                    max_photo = url_photo
                    break
                elif url_photo['height'] > max_photo['height'] or url_photo['width'] > max_photo['width'] :
                    max_photo = url_photo
            photo[count_photo] = max_photo
            photo[count_photo]['likes'] = p['likes']['count']
            count_photo += 1
        print('Выбираем фото: ')
        x = 0
        while x < NPh:
            photo_NPh[x] = photo[x]
            x += 1
        if len(photo) <= NPh: # если фото меньше заданного, то забираем все фото
            print('Все фото выбраны')
        else:
            j=0
            for i in tqdm(photo_NPh):
                sleep(1)
                for j in photo:
                    if photo[j]['height'] > photo_NPh[i]['height']:
                        photo_NPh[i] = photo[j]
                    break
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


    def upload(self, path_file, photos):  # записываем файлы на Ядиск
        file_for_json = []                    # собираем словарь для файла json
        i = 0
        print('\n',"Грузим фото в яднекс")
        # используем прогресс-бар
        for photo in tqdm(photos):
            sleep(1)
            self.param['url'] = photos[photo]['url']
            file_for_json.append({'file_name': '', 'size': ''})
            path_disk = path_file + "/" + str(photo)  + str(photos[photo]['likes']) + '.'+'jpeg'
            file_for_json[i]['file_name'] += path_disk
            file_for_json[i]['size'] += photos[photo]['type']
            self.param['path'] = path_disk
            i += 1
            r = requests.post(url=self.url, params=self.param, headers=self.heads).json
        #записываем файл json
        with open("photos.json", "w") as file:
            json.dump(file_for_json, file, indent=3)

        return



if __name__ == '__main__':
    vk_id = 739978517
    vktoken = ''

    Number_photo = 5
    name_dir = 'vk_pic'
    token = ''
    mevk = MyVk()
    vk_photo = mevk.get_photos(Number_photo)
    uploader = YaUploader(token)
    uploader.heads
    uploader.get_headers(name_dir,vk_photo)
    path_file = uploader.mk_dir(name_dir)
    result = uploader.upload(name_dir,vk_photo)
    print(result)

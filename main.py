import requests,json, time, os
import yadisk
import pprint


vk_id = 739978517
vktoken = "vk1.a.6B5LBGoSQK41T7B9rTJf4WaiGjQPeZ5nSlJHpDYrt6h7hxIL2xUPW0twZMI8gZTOOUg9DSBH-mcVydncjrpHvQ9dUCUUL77wxCx7APZ4Hrywa3IqQ9RkRQhTnNNcIhDq3qWPA5q8R1fRNY_fou15PDMkUSd1tGc_osCFkY9dpASK-GzYmjK985ZvJie-rL3O"
token = 'AQAAAAA3hrAhAADLW6iygdsEFkmmmDqlFp35p-U'


class MyVk:  # объявляем класс вк
    def __init__(self):
        self.token = "vk1.a.6B5LBGoSQK41T7B9rTJf4WaiGjQPeZ5nSlJHpDYrt6h7hxIL2xUPW0twZMI8gZTOOUg9DSBH-mcVydncjrpHvQ9dUCUUL77wxCx7APZ4Hrywa3IqQ9RkRQhTnNNcIhDq3qWPA5q8R1fRNY_fou15PDMkUSd1tGc_osCFkY9dpASK-GzYmjK985ZvJie-rL3O"
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
        for url_photo in my_data:
            photo[str(count_photo)] = url_photo['height'],url_photo['width'],url_photo['url'],url_photo['type']
            count_photo += 1
        i = 0
        if len(photo) <= NPh : # если фото меньше заданного, то забираем все фото
            photo1 = photo
        else:
            for i in range(len(photo)):
                if len(photo_NPh) < NPh :
                    photo_NPh[str(i)] = photo[str(i)]
                else:
                    for j in range(len(photo_NPh)):  # если фото больше - начинаем выбирать нужные фото
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

    def get_headers(self,path_to_file,file_name,):  # подбираем параметры, необходимые для записи на Ядиск
        self.heads = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        self.param = {'url':'','path':'', 'overwrite': 'true'}
        self.dirparam = {'path':path_to_file, 'overwrite': 'true'}
        return

    def mk_dir(self,file_path: str):  # создаем каталог на Ядиске (имя каталога не задано)
        mkurl = 'https://cloud-api.yandex.net/v1/disk/resources/'
        requests.put(url=mkurl, params=self.dirparam, headers=self.heads).json()


    def upload(self, path_file, photos,likes):  # записываем файлы на Ядиск
        file_for_json = {}                      # собираем словарь для файла json
        file_for_json['file_name'] = []
        file_for_json['size'] = []
        for photo in photos.values():
            self.param['url'] = photo[2]
            path_disk = path_file + "/" + str(photo[0])  + str(likes) + '.'+'jpeg'
            file_for_json['file_name'].append(path_disk)
            file_for_json['size'].append(photo[3])
            self.param['path'] = path_disk

            r = requests.post(url=self.url,params=self.param,headers=self.heads).json
        print(file_for_json)

        #requests.get(url=self.url, params=self.param, headers=self.heads).json
        return



if __name__ == '__main__':
    mevk = MyVk()
    Number_photo = 5
    vk_photo = mevk.get_photos(Number_photo)
    name_dir = 'vk_pic'
    uploader = YaUploader(token)
    uploader.get_headers(name_dir,vk_photo)
    path_file = uploader.mk_dir(name_dir)
    result = uploader.upload(name_dir,vk_photo,mevk.likes)


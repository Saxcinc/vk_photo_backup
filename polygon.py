import requests
import tqdm


class Polygon():

    ya_disk_url = "https://cloud-api.yandex.net/v1/disk/resources"
    
    
    def __init__(self, ya_token, folder_name, vk_client):
        self.ya_token = ya_token
        self.folder_name = folder_name
        self.vk_client = vk_client


    def _check_name_folder(self):

        headers = {"Authorization": f"OAuth {self.ya_token}"}
        params = {"path": self.folder_name}

        response = requests.get(self.ya_disk_url, headers=headers, params=params)

        return response.status_code == 200


    def _create_folder(self):
        '''Функция создает папку на Я.Диске'''

        headers = {"Authorization": f"OAuth {self.ya_token}"}
        params = {"path": f"{self.folder_name}"}

        response = requests.put(f"{self.ya_disk_url}", headers=headers, params=params)

        return response
         

    def save_photo(self):
        '''Функция сохраняет фотографии на Я.Диск в именованную пользователем папку'''

        self._create_folder()
        all_data = self.vk_client._get_max_photo_size()
        headers = {"Authorization": f"OAuth {self.ya_token}"}
        print("\nПолучаем данные... Загружаем...\n")

        for get_name, get_url in tqdm.tqdm(all_data.items()):
            params = {"path": f"{self.folder_name}/{get_name}", "url": f"{get_url["url"]}"}
            response = requests.post(f"{self.ya_disk_url}/upload?", headers=headers, params=params)


    def publish_folder(self):
        '''Делает папку публичной'''

        headers = {"Authorization": f"OAuth {self.ya_token}"}
        params = {"path": self.folder_name}

        response = requests.put(f"{self.ya_disk_url}/publish", headers=headers, params=params)

        if response.status_code == 200:
            print(f"Папка '{self.folder_name}' успешно опубликована.")
            return response.json().get('href')
        else:
            print(f"Ошибка при публикации папки: {response.status_code}")
            return None

from operator import itemgetter
import requests


class VK():

    vk_url = "https://api.vk.com/method"

    def __init__(self, user_id, service_token) -> None:
        self.user_id = user_id
        self.service_token_vk = service_token

    def _get_params(self) -> None:

        return {
            "access_token": self.service_token_vk,
            "v": "5.199",
            "count": 5
        }
    
    def _get_info_profile(self):
        '''Возвращает json файл о полученных фотографиях с профиля пользователя'''
        params = self._get_params()
        params.update({"owner_id": self.user_id, "album_id": "profile", "extended": 1})
        
        
        response = requests.get(f"{self.vk_url}/photos.get?", params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Произошла ошибка, статус: {response.status_code}")
            return None

    def _get_max_photo_size(self):
        """Функция возвращает информацию о полученных фотографиях"""

        all_data_photos = self._get_info_profile()
        photos_info = {}

        for item_photo_info in all_data_photos["response"]["items"]:
            if item_photo_info["likes"]["count"] not in photos_info:
                sorted_size_all = sorted(item_photo_info["sizes"], key=itemgetter("height"))

                dict_info = {
                    item_photo_info["likes"]["count"]: {
                        "size": f"{item_photo_info["sizes"][-1]["type"]}",
                        "url": f"{item_photo_info["sizes"][-1]["url"]}",
                    }
                }
                photos_info.update(dict_info)
            else:
                dict_info = {
                    str(item_photo_info["likes"]["count"]) + str(item_photo_info["date"]): {
                        "size": f"{sorted_size_all[-1]['type']}",
                        "url": f"{sorted_size_all[-1]['url']}"}                    
                        }
                photos_info.update(dict_info)

        return photos_info
    
    def output_photo_info(self):
        """Функция записывает в json информацию о файлах, которые были сохранены на Я.Диск"""

        all_data_photos = self._get_max_photo_size()
        output = []

        for key, value in all_data_photos.items():
            output_info = {
                "file_name": f"{key}.jpg",
                "size": f"{value["size"]}",
            }
            output.append(output_info)

        return output
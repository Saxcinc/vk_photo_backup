import json
from polygon import Polygon
from vk import VK

def save_data_to_json(data, filename):

    with open(filename, "w") as file:
        json.dump(data, file)

def main():

    user_id = str(input("Введите id пользователя VK: "))
    service_token_vk = str(input("Введите сервисный ключ VK: "))
    polygon_token = str(input("Введите OAuth токен от Я.Диска: "))
    folder_name = str(input("Создание новой папки для выгрузки фото, укажите название: "))

    vk_rec = VK(user_id, service_token_vk)
    polygon_rec = Polygon(polygon_token, folder_name, vk_rec)

    if polygon_rec._check_name_folder():
        print("Папка с таким именем уже существует!\n")
        user_choice = input("Выберите действие:\n\n[1] - Сохранить в существующую\n[2] - Создать новую папку\n> ")
        if user_choice == "2":
            new_folder_name = input("Введите новое имя для папки: ")
            polygon_rec.folder_name = new_folder_name

    photo_info = vk_rec.output_photo_info()
    save_data_to_json(photo_info, 'info_data.json')
    polygon_rec.save_photo()
    print(f"\nДанные успешно загружены в папку '{polygon_rec.folder_name}'.")

    public_url = polygon_rec.publish_folder()
    
    if public_url:
        print(f"Ссылка на папку: https://disk.yandex.ru/client/disk/{polygon_rec.folder_name}")

if __name__ == "__main__":
    main()
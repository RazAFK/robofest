import os
import shutil
import random

def split_dataset(source_dir, train_ratio=0.8):
    # Определяем пути
    dataset_dir = os.path.join(source_dir, 'dataset')
    folders = [
        'train/images', 'train/labels',
        'val/images', 'val/labels'
    ]
    
    # 1. Создаем структуру папок
    for folder in folders:
        os.makedirs(os.path.join(dataset_dir, folder), exist_ok=True)

    # 2. Собираем список всех изображений (ищем только файлы .jpg)
    images = [f for f in os.listdir(source_dir) if f.endswith('.jpg')]
    random.shuffle(images) # Перемешиваем для честного разделения

    split_idx = int(len(images) * train_ratio)
    train_files = images[:split_idx]
    val_files = images[split_idx:]

    def move_files(files, subset):
        for img_name in files:
            # Имя файла без расширения
            base_name = os.path.splitext(img_name)[0]
            label_name = base_name + '.txt'

            # Пути "ОТКУДА"
            img_src = os.path.join(source_dir, img_name)
            label_src = os.path.join(source_dir, label_name)

            # Проверяем, есть ли файл разметки для фото
            if not os.path.exists(label_src):
                print(f"Пропуск: нет разметки для {img_name}")
                continue

            # Пути "КУДА"
            shutil.copy(img_src, os.path.join(dataset_dir, subset, 'images', img_name))
            shutil.copy(label_src, os.path.join(dataset_dir, subset, 'labels', label_name))

    # 3. Раскладываем файлы
    move_files(train_files, 'train')
    move_files(val_files, 'val')

    print(f"Готово! Разделено: {len(train_files)} в train, {len(val_files)} в val.")
    print(f"Путь к датасету: {dataset_dir}")

if __name__ == "__main__":
    # Укажите путь к папке, где сейчас лежат все фото и txt вместе
    source_path = 'C:/Users/admin/Desktop/wroom_wroom/'
    split_dataset(source_path)

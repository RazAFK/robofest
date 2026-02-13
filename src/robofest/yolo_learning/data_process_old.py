import cv2

def select_objects(image_path):
    # Загружаем изображение
    image = cv2.imread(image_path)
    if image is None:
        print("Ошибка: не удалось загрузить изображение.")
        return

    # Список для хранения данных: [[x, y, w, h], "название_класса"]
    labeled_objects = []

    print("ИНСТРУКЦИЯ:")
    print("1. Выделите объект мышкой")
    print("2. Нажмите ENTER или SPACE для подтверждения рамки")
    print("3. Введите название класса в консоли")
    print("4. Повторите для других объектов")
    print("5. Нажмите ESC, когда закончите выделение всех объектов")

    # Позволяет выделить несколько областей (Region of Interest)
    # showCrosshair=True рисует перекрестие, fromCenter=False выделение от угла
    rects = cv2.selectROIs("Annotation Window", image, showCrosshair=True, fromCenter=False)

    for i, rect in enumerate(rects):
        # Рисуем временную рамку, чтобы понимать, какой объект подписываем
        x, y, w, h = rect
        temp_img = image.copy()
        cv2.rectangle(temp_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("Annotation Window", temp_img)
        cv2.waitKey(1)

        # Запрашиваем имя класса в консоли
        class_name = input(f"Введите название класса для объекта {i+1}: ")
        labeled_objects.append({"box": rect, "class": class_name})

    cv2.destroyAllWindows()

    # Вывод результата
    print("\nИтоговая разметка:")
    for obj in labeled_objects:
        print(f"Класс: {obj['class']}, Координаты [x, y, w, h]: {obj['box']}")

if __name__ == "__main__":
    # Укажите путь к вашему фото
    select_objects('C:/Users/admin/Desktop/cube_photos/1.jpg')

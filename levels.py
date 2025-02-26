"""
Модуль управления уровнями и таблицей рекордов.
Содержит:
  - Класс Level для отслеживания текущего уровня и перехода между ними.
  - Функции load_records, save_record и draw_records для работы с таблицей рекордов.
"""

import os
import json
import pygame

# Файл для сохранения рекордов
RECORDS_FILE = 'records.json'


def load_records():
    """
    Загружает рекорды из файла RECORDS_FILE.
    Если файл не существует, возвращает пустой список.
    """
    if os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, 'r') as f:
            return json.load(f)
    return []


def save_record(name, score):
    """
    Сохраняет новый рекорд.

    Аргументы:
      name - имя игрока.
      score - набранное количество очков.

    Рекорды сортируются по убыванию, сохраняется топ-10.
    """
    records = load_records()
    records.append({'name': name, 'score': score})
    records.sort(key=lambda x: x['score'], reverse=True)
    with open(RECORDS_FILE, 'w') as f:
        json.dump(records[:10], f)


def draw_records(screen):
    """
    Отрисовывает таблицу рекордов в левом верхнем углу экрана.

    Аргументы:
      screen - поверхность для отрисовки.
    """
    font = pygame.font.SysFont("Arial", 24)
    records = load_records()
    y_offset = 10  # Начинаем с небольшого отступа от верхнего края
    title_text = font.render("Рекорды:", True, (255, 255, 255))
    screen.blit(title_text, (10, y_offset))
    y_offset += title_text.get_height() + 5
    for i, record in enumerate(records[:5]):  # Показываем топ-5 рекордов
        text = font.render(
            f"{i+1}. {record['name']} - {record['score']}", True, (255, 255, 255))
        screen.blit(text, (10, y_offset))
        y_offset += text.get_height() + 5


class Level:
    def __init__(self, number):
        """
        Инициализирует уровень.

        Аргументы:
          number - начальный номер уровня.
        """
        self.number = number

    def next_level(self):
        """
        Переходит на следующий уровень.
        Можно усложнять игру, увеличивая скорость врагов или добавляя новые типы.
        """
        self.number += 1
        print(f"Переход на уровень {self.number}")

# Дополнительные комментарии:
# Модуль levels.py объединяет логику уровней и работу с таблицей рекордов.
# Функции для загрузки/сохранения рекордов позволяют сохранять топ-10 результатов.
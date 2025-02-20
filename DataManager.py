import os
import sqlite3
import pygame

class GameDataManager:
    def __init__(self, db_path='data/data.sqlite'):
        self.db_path = db_path
        self.init_db()
        self.init_default_settings()
        self.init_default_music()

    def init_db(self):
        # Инициализация базы данных и создание таблиц, если они не существуют.
        if not os.path.exists('data'):
            os.makedirs('data')

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Создание таблицы настроек, если она не существует
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    name TEXT PRIMARY KEY,
                    value TEXT,
                    language TEXT
                )
            ''')
            # Создание таблицы звуков, если она не существует
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sound (
                    section TEXT,
                    path TEXT
                )
            ''')
            conn.commit()

    def init_default_settings(self):
        # Инициализация настроек по умолчанию, если они отсутствуют.
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Проверяем, существует ли настройка 'volume'
            cursor.execute('SELECT value FROM settings WHERE name = ?', ('volume',))
            result = cursor.fetchone()

            if result is None:
                self.set_setting("volume", '10')
            # Существование языка
            cursor.execute('SELECT value FROM settings WHERE name = ?', ('language',))
            result = cursor.fetchone()
            print(result)
            if result is None:
                self.set_setting("language", 'ENG')


    def init_default_music(self):
        self.set_sound("menu", "data\Хоккейный гимн.mp3")
        self.set_sound("game", "data\sound_arena.mp3")


    def get_setting(self, name):
        # Получение значения настройки по имени.
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM settings WHERE name = ?', (name,))
            result = cursor.fetchone()
            return result[0] if result else None

    def set_setting(self, name, value):
        # Установка или обновление значения настройки.
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('REPLACE INTO settings (name, value) VALUES (?, ?)', (name, value))
            conn.commit()

    def load_sound(self, section):
        # Загрузка звуков по разделу игры (меню, сама игра).
        sound = None
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT path FROM sound WHERE section = ?', (section,))
            for row in cursor.fetchall():
                path = row[0]
                if os.path.exists(path):
                    sound = pygame.mixer.Sound(path)
                else:
                    print(f"Файл не найден: {path}")
        return sound

    def set_sound(self, name, path_track):
        # Установка или обновление значения настройки.
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('REPLACE INTO sound (section, path) VALUES (?, ?)', (name, path_track))
            conn.commit()

if __name__ == "__main__":
    manager = GameDataManager()
    manager.set_setting('volume', '0')
    print(manager.get_setting('volume'))

    # Загрузка и проигрывание звуков
    sounds = manager.load_sound('main_menu')
    for sound in sounds:
        manager.play_sound(sound)
import os
import shutil
import stat
import pathlib
from datetime import datetime

class FileManager:
    def __init__(self):
        self.current_path = os.getcwd()

    def get_current_path(self):
        return os.getcwd()

    def list_contents(self):
        """Просмотр содержимого текущей директории (Файлы и Каталоги)"""
        print(f"\n--- Содержимое: {self.current_path} ---")
        try:
            items = os.listdir(self.current_path)
            for item in items:
                full_path = os.path.join(self.current_path, item)
                item_type = "[DIR]" if os.path.isdir(full_path) else "[FILE]"
                print(f"{item_type} {item}")
        except PermissionError:
            print("Ошибка: Нет прав доступа к этой папке.")

    def create_item(self, name, is_dir=False):
        """Создание файла или каталога"""
        path = os.path.join(self.current_path, name)
        try:
            if is_dir:
                os.mkdir(path)
                print(f"Папка '{name}' создана.")
            else:
                with open(path, 'w') as f:
                    pass
                print(f"Файл '{name}' создан.")
        except FileExistsError:
            print("Ошибка: Объект с таким именем уже существует.")
        except Exception as e:
            print(f"Ошибка создания: {e}")

    def delete_item(self, name):
        """Удаление файла или каталога"""
        path = os.path.join(self.current_path, name)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path) # Удаляет папку рекурсивно
                print(f"Папка '{name}' удалена.")
            else:
                os.remove(path)
                print(f"Файл '{name}' удален.")
        except FileNotFoundError:
            print("Ошибка: Объект не найден.")
        except Exception as e:
            print(f"Ошибка удаления: {e}")

    def rename_item(self, old_name, new_name):
        """Переименование"""
        old_path = os.path.join(self.current_path, old_name)
        new_path = os.path.join(self.current_path, new_name)
        try:
            os.rename(old_path, new_path)
            print(f"Переименовано: '{old_name}' -> '{new_name}'")
        except Exception as e:
            print(f"Ошибка переименования: {e}")

    def copy_item(self, source_name, dest_path=None):
        """Копирование"""
        source = os.path.join(self.current_path, source_name)
        # Если путь назначения не указан, копируем в текущую папку с именем copy_...
        if not dest_path:
            dest = os.path.join(self.current_path, "copy_" + source_name)
        else:
            dest = os.path.join(dest_path, source_name)
        
        try:
            if os.path.isdir(source):
                shutil.copytree(source, dest)
            else:
                shutil.copy2(source, dest)
            print(f"Скопировано в: {dest}")
        except Exception as e:
            print(f"Ошибка копирования: {e}")

    def move_item(self, source_name, dest_path):
        """Перемещение"""
        source = os.path.join(self.current_path, source_name)
        dest = os.path.join(dest_path, source_name)
        try:
            shutil.move(source, dest)
            print(f"Перемещено в: {dest}")
        except Exception as e:
            print(f"Ошибка перемещения: {e}")

    def get_info(self, name):
        """Просмотр свойств и атрибутов"""
        path = os.path.join(self.current_path, name)
        try:
            stat_info = os.stat(path)
            print(f"\n--- Информация: {name} ---")
            print(f"Размер: {stat_info.st_size} байт")
            print(f"Время создания: {datetime.fromtimestamp(stat_info.st_ctime)}")
            print(f"Время изменения: {datetime.fromtimestamp(stat_info.st_mtime)}")
            print(f"Права (Unix): {oct(stat_info.st_mode)}")
            print(f"Только чтение: {bool(stat_info.st_mode & stat.S_IREAD)}")
        except Exception as e:
            print(f"Ошибка получения информации: {e}")

    def set_permissions(self, name, mode):
        """Изменение прав доступа (например, 0o755)"""
        path = os.path.join(self.current_path, name)
        try:
            # mode должен быть в восьмеричном формате, например 0o777
            os.chmod(path, mode)
            print(f"Права для '{name}' изменены на {oct(mode)}.")
        except Exception as e:
            print(f"Ошибка изменения прав: {e}")

    def search(self, pattern):
        """Поиск файлов по маске"""
        print(f"\n--- Поиск по маске: {pattern} ---")
        try:
            # Используем pathlib для удобного поиска
            path_obj = pathlib.Path(self.current_path)
            matches = list(path_obj.glob(pattern))
            if matches:
                for m in matches:
                    print(m.name)
            else:
                print("Ничего не найдено.")
        except Exception as e:
            print(f"Ошибка поиска: {e}")

    def change_directory(self, path):
        """Переход в другую директорию (Открытие каталога)"""
        if path == '..':
            new_path = os.path.dirname(self.current_path)
        else:
            new_path = os.path.join(self.current_path, path)
        
        if os.path.isdir(new_path):
            os.chdir(new_path)
            self.current_path = os.getcwd()
            print(f"Переход в: {self.current_path}")
        else:
            print("Ошибка: Директория не найдена.")

    def edit_file(self, name):
        """Простое редактирование текстового файла"""
        path = os.path.join(self.current_path, name)
        if os.path.isfile(path):
            print(f"Редактирование {name} (введите текст, завершите пустой строкой):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            
            try:
                with open(path, 'w') as f:
                    f.write('\n'.join(lines))
                print("Файл сохранен.")
            except Exception as e:
                print(f"Ошибка записи: {e}")
        else:
            print("Ошибка: Это не файл.")

def main():
    fm = FileManager()
    print("=== Файловый менеджер (Лабораторная №4) ===")
    
    while True:
        print(f"\nПуть: {fm.get_current_path()}")
        print("1. Просмотр содержимого")
        print("2. Создать файл")
        print("3. Создать папку")
        print("4. Удалить")
        print("5. Переименовать")
        print("6. Копировать")
        print("7. Переместить")
        print("8. Свойства/Атрибуты")
        print("9. Изменить права (chmod)")
        print("10. Поиск")
        print("11. Перейти в папку (cd)")
        print("12. Редактировать файл")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            fm.list_contents()
        elif choice == '2':
            name = input("Имя файла: ")
            fm.create_item(name, is_dir=False)
        elif choice == '3':
            name = input("Имя папки: ")
            fm.create_item(name, is_dir=True)
        elif choice == '4':
            name = input("Имя объекта для удаления: ")
            fm.delete_item(name)
        elif choice == '5':
            old = input("Старое имя: ")
            new = input("Новое имя: ")
            fm.rename_item(old, new)
        elif choice == '6':
            name = input("Имя объекта для копирования: ")
            dest = input("Путь назначения (оставьте пустым для текущей папки): ")
            fm.copy_item(name, dest if dest else None)
        elif choice == '7':
            name = input("Имя объекта для перемещения: ")
            dest = input("Путь назначения: ")
            fm.move_item(name, dest)
        elif choice == '8':
            name = input("Имя объекта: ")
            fm.get_info(name)
        elif choice == '9':
            name = input("Имя объекта: ")
            try:
                mode = int(input("Режим прав (например, 755): "), 8)
                fm.set_permissions(name, mode)
            except ValueError:
                print("Ошибка: Введите число в восьмеричном формате.")
        elif choice == '10':
            pattern = input("Маска поиска (например, *.txt): ")
            fm.search(pattern)
        elif choice == '11':
            path = input("Путь (или .. для назад): ")
            fm.change_directory(path)
        elif choice == '12':
            name = input("Имя файла для редактирования: ")
            fm.edit_file(name)
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверная команда.")

if __name__ == "__main__":
    main()

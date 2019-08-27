import os
import sys
from main_class import DataBaseManager

if __name__ == "__main__":
    data_base_manager = DataBaseManager()
    if '-h' in sys.argv or '--help' in sys.argv:
        print("""
            --create_table создание таблицы для персонала \n
            --load_json_data загрузка данных из json файла \n
            --show_persons_in_city вывод всех сотрудников работающих в городе.
            Пример использования --show_persons_in_city [id] работника
            """)

    if '--create_table' in sys.argv:
        data_base_manager.create_persons_table()
    if '--load_json_data' in sys.argv:
        data_base_manager.set_data_from_json()
    if '--show_persons_in_city' in sys.argv:
        user_id = sys.argv[sys.argv.index('--show_persons_in_city')+1]
        draw_data = data_base_manager.get_draw_data_all_persons_in_city(
            user_id
        )
        print('Персонал в городе %s' % draw_data['city_name'])
        print(draw_data['persons_list'])

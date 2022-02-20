import logging

import psycopg2
from key import user, password, host, port

#
# class BotDB:
#
#     def __init__(self):
#         """Инициализация подключения БД"""
#         self.conn = psycopg2.connect(user=user,
#                                      password=password,
#                                      host=host,
#                                      port=port,
#                                      dbname='firstbase1')
#         self.cur = self.conn.cursor()
#
#     def get_all_records(self):
#         """Получить все строки"""
#         query = "select * from people;"
#         self.cur.execute(query)
#         res = self.cur.fetchall()
#         return res
#
#     def get_friends(self):
#         """Получаем список друзей для проверки дней рождений"""
#         query = "select persone_name, birthday_date from people where type_persons = '1';"
#         self.cur.execute(query)
#         res = self.cur.fetchall()
#         # print(res)
#         return res
#
#     def get_colleagues(self):
#         """Получаем список коллег для проверки дней рождений"""
#         query = "select persone_name, birthday_date from people p where p.type_persons = '2';"
#         self.cur.execute(query)
#         res = self.cur.fetchall()
#         # print(res)
#         return res
#
#     def add_birthday(self, p_name, p_date, p_type):
#         """Добавляем новую запись о дне рождения в таблицу"""
#         try:
#             query = """INSERT INTO people (persone_name, birthday_date, type_persons) values (%s,%s,%s)"""
#             values = (str(p_name), str(p_date), str(p_type),)
#             self.cur.execute(query, values)
#             self.conn.commit()
#             return True
#         except Exception as e:
#             print("Ошибка при вставке {}", e)
#             return False
#
#     def del_by_id(self, id):
#         """Удаляем запись о дне рождении по ID"""
#         try:
#             self.cur.execute("delete from people p where p.id = %s", (id,))
#             self.conn.commit()
#             return True
#         except:
#             return False
#
#     def find_by_surname(self, surname, tp):
#         if tp == 2:
#             self.cur.execute("select * from people p where p.persone_name like %s "
#                              "and p.type_persons = %s::varchar ", (surname, tp,))
#             res = self.cur.fetchall()
#             if res:
#                 return res
#             else:
#                 return False
#         elif tp == 1:  # private
#             self.cur.execute("select * from people p where p.persone_name like %s ", (surname,))
#             res = self.cur.fetchall()
#             if res:
#                 return res
#             else:
#                 return False
#
#     def getinfo(self):
#         return self.conn.info
#
#     def close(self):
#         """Закрытие соединения с БД"""
#         self.conn.close()

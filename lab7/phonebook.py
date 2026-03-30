import csv
from connect import get_connection

def init_db():
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS phonebook (name VARCHAR(255) PRIMARY KEY, phone VARCHAR(20));")
        conn.commit()
        cur.close()
        conn.close()

def import_from_csv(filename):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING", row)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Данные из CSV импортированы.")

def main_menu():
    init_db()
    while True:
        print("\n1. Импорт CSV | 2. Добавить | 3. Поиск | 4. Обновить | 5. Удалить | 6. Выход")
        choice = input("Выбор: ")
        
        conn = get_connection()
        cur = conn.cursor()
        
        if choice == '1':
            import_from_csv('contacts.csv')
        elif choice == '2':
            name, phone = input("Имя: "), input("Телефон: ")
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET phone = EXCLUDED.phone", (name, phone))
        elif choice == '3':
            name = input("Имя для поиска: ")
            cur.execute("SELECT * FROM phonebook WHERE name LIKE %s", (name + '%',))
            for r in cur.fetchall(): print(f"👤 {r[0]}: {r[1]}")
        elif choice == '4':
            name, phone = input("Кому меняем? "), input("Новый телефон: ")
            cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (phone, name))
        elif choice == '5':
            name = input("Кого удалить? ")
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
        elif choice == '6':
            break
        
        conn.commit()
        cur.close()
        conn.close()

if __name__ == "__main__":
    main_menu()

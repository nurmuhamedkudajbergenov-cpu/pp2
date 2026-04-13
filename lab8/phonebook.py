import csv
from connect import get_connection

def show_paged(page=0):
    limit = 5  # Показываем по 5 контактов за раз
    offset = page * limit
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_paged(%s, %s);", (limit, offset))
        rows = cur.fetchall()
        print(f"\n--- СТРАНИЦА {page + 1} ---")
        for r in rows: print(f"{r[0]:<20} | {r[1]:<15}")
        cur.close()
        conn.close()
    return len(rows)

def main_menu():
    current_page = 0
    while True:
        has_data = show_paged(current_page)
        print("\n1. Импорт (Bulk) | 2. Add/Update | 3. Поиск | 4. Удалить | 5. След. стр | 0. Выход")
        choice = input("Выбор: ")
        
        conn = get_connection()
        cur = conn.cursor()

        if choice == '0': break
        elif choice == '1':
            with open('contacts.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    # В реальной жизни тут можно добавить проверку regex для телефона
                    cur.execute("CALL upsert_contact(%s, %s)", row)
            print("✅ Массовый импорт завершен.")
        elif choice == '2':
            cur.execute("CALL upsert_contact(%s, %s)", (input("Имя: "), input("Телефон: ")))
        elif choice == '3':
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (input("Поиск: "),))
            for r in cur.fetchall(): print(f"🔍 Найдено: {r[0]} - {r[1]}")
            input("Нажми Enter...")
        elif choice == '4':
            cur.execute("CALL delete_contact(%s)", (input("Кого удалить? "),))
        elif choice == '5':
            current_page = current_page + 1 if has_data == 5 else 0

        conn.commit()
        cur.close()
        conn.close()

if __name__ == "__main__":
    main_menu()

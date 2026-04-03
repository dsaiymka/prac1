import csv
from connect import get_connection

# ---------- HELPERS ----------
def is_valid_phone(phone):
    phone = phone.strip()
    return phone.isdigit() or (phone.startswith('+') and phone[1:].isdigit())

def print_contacts(rows):
    if not rows:
        print("Контакты не найдены.")
        return

    print("\nID | NAME | PHONE")
    print("-" * 30)
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]}")

# ---------- CREATE ----------
def insert_from_csv(filename):
    conn = get_connection()
    if not conn:
        print("Не удалось подключиться к базе данных!")
        return

    cur = conn.cursor()

    # --- создаём уникальный индекс на (name, phone), если его ещё нет ---
    try:
        cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS unique_name_phone ON contacts(name, phone);")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Ошибка при создании индекса:", e)

    # --- импорт CSV ---
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get('name', '').strip()
                phone = row.get('phone', '').strip()

                if not name or not phone:
                    print("Пропущена некорректная строка:", row)
                    continue

                if not is_valid_phone(phone):
                    print(f"Некорректный телефон пропущен: {phone}")
                    continue

                cur.execute("""
                    INSERT INTO contacts (name, phone)
                    VALUES (%s, %s)
                    ON CONFLICT (name, phone) DO NOTHING
                """, (name.title(), phone))

        conn.commit()
        print("Импорт CSV завершён.")
    except Exception as e:
        conn.rollback()
        print("Ошибка:", e)
    finally:
        cur.close()
        conn.close()

def insert_from_console():
    name = input("Введите имя: ").strip().title()
    phone = input("Введите телефон: ").strip()

    if not is_valid_phone(phone):
        print("Некорректный телефон!")
        return

    conn = get_connection()
    if not conn:
        print("Не удалось подключиться к базе данных!")
        return

    cur = conn.cursor()
    try:
        # создаём индекс, если ещё не существует
        cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS unique_name_phone ON contacts(name, phone);")
        conn.commit()
    except:
        conn.rollback()

    try:
        cur.execute("""
            INSERT INTO contacts (name, phone)
            VALUES (%s, %s)
            ON CONFLICT (name, phone) DO NOTHING
        """, (name, phone))

        if cur.rowcount == 0:
            print("Такой контакт уже существует.")
        else:
            print("Контакт добавлен.")

        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Ошибка:", e)
    finally:
        cur.close()
        conn.close()

# ---------- READ ----------
def query_contacts():
    conn = get_connection()
    if not conn:
        print("Не удалось подключиться к базе данных!")
        return

    cur = conn.cursor()
    print("\n1. Показать все контакты")
    print("2. Поиск по имени")
    print("3. Поиск по префиксу телефона")

    choice = input("Выберите: ")
    try:
        if choice == "1":
            cur.execute("SELECT * FROM contacts")
        elif choice == "2":
            name = input("Введите имя: ").strip()
            cur.execute("SELECT * FROM contacts WHERE name ILIKE %s", (f"%{name}%",))
        elif choice == "3":
            prefix = input("Введите префикс: ").strip()
            cur.execute("SELECT * FROM contacts WHERE phone LIKE %s", (f"{prefix}%",))
        else:
            print("Некорректный выбор!")
            return

        rows = cur.fetchall()
        print_contacts(rows)

    except Exception as e:
        print("Ошибка:", e)
    finally:
        cur.close()
        conn.close()

# ---------- UPDATE ----------
def update_contact():
    conn = get_connection()
    if not conn:
        print("Не удалось подключиться к базе данных!")
        return

    cur = conn.cursor()
    print("\nОбновить по:")
    print("1. ID")
    print("2. Телефону")

    choice = input("Выберите: ")
    try:
        if choice == "1":
            try:
                contact_id = int(input("Введите ID: "))
            except ValueError:
                print("Некорректный ID!")
                return

            field = input("Что обновить (name/phone): ").strip().lower()
            if field == "name":
                new_name = input("Новое имя: ").strip().title()
                cur.execute("UPDATE contacts SET name=%s WHERE id=%s", (new_name, contact_id))
            elif field == "phone":
                new_phone = input("Новый телефон: ").strip()
                if not is_valid_phone(new_phone):
                    print("Некорректный телефон!")
                    return
                cur.execute("UPDATE contacts SET phone=%s WHERE id=%s", (new_phone, contact_id))
            else:
                print("Некорректное поле!")
                return
        elif choice == "2":
            phone = input("Введите текущий телефон: ").strip()
            new_phone = input("Новый телефон: ").strip()
            if not is_valid_phone(new_phone):
                print("Некорректный телефон!")
                return
            cur.execute("UPDATE contacts SET phone=%s WHERE phone=%s", (new_phone, phone))
        else:
            print("Некорректный выбор!")
            return

        if cur.rowcount == 0:
            print("Контакт не найден.")
        else:
            print("Обновлено успешно.")

        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Ошибка:", e)
    finally:
        cur.close()
        conn.close()

# ---------- DELETE ----------
def delete_contact():
    conn = get_connection()
    if not conn:
        print("Не удалось подключиться к базе данных!")
        return

    cur = conn.cursor()
    print("\nУдалить по:")
    print("1. ID")
    print("2. Телефону")

    choice = input("Выберите: ")
    try:
        if choice == "1":
            try:
                contact_id = int(input("Введите ID: "))
            except ValueError:
                print("Некорректный ID!")
                return
            cur.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
        elif choice == "2":
            phone = input("Введите телефон: ").strip()
            cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))
        else:
            print("Некорректный выбор!")
            return

        if cur.rowcount == 0:
            print("Контакт не найден.")
        else:
            print("Удалено успешно.")

        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Ошибка:", e)
    finally:
        cur.close()
        conn.close()

# ---------- MENU ----------
def menu():
    while True:
        print("\n=== ТЕЛЕФОННАЯ КНИГА ===")
        print("1. Импорт из CSV")
        print("2. Добавить контакт")
        print("3. Просмотр/поиск контактов")
        print("4. Обновить контакт")
        print("5. Удалить контакт")
        print("6. Выход")

        choice = input("Выберите опцию: ")
        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            query_contacts()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Некорректный выбор!")

if __name__ == "__main__":
    menu()
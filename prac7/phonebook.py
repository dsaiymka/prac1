import csv
from connect import get_connection


# ---------- HELPERS ----------
def is_valid_phone(phone):
    phone = phone.strip()
    return phone.isdigit() or (phone.startswith('+') and phone[1:].isdigit())


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    print("\nID | NAME | PHONE")
    print("-" * 30)
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]}")


# ---------- CREATE ----------
def insert_from_csv(filename):
    conn = get_connection()
    if not conn:
        print("Database connection failed!")
        return

    cur = conn.cursor()

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get('name', '').strip()
                phone = row.get('phone', '').strip()

                if not name or not phone:
                    print("Skipping invalid row:", row)
                    continue

                if not is_valid_phone(phone):
                    print(f"Invalid phone skipped: {phone}")
                    continue

                cur.execute("""
                    INSERT INTO contacts (name, phone)
                    VALUES (%s, %s)
                    ON CONFLICT (phone) DO NOTHING
                """, (name.title(), phone))

        conn.commit()
        print("CSV import completed.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


def insert_from_console():
    name = input("Enter name: ").strip().title()
    phone = input("Enter phone: ").strip()

    if not is_valid_phone(phone):
        print("Invalid phone number!")
        return

    conn = get_connection()
    if not conn:
        print("Database connection failed!")
        return

    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO contacts (name, phone)
            VALUES (%s, %s)
            ON CONFLICT (phone) DO NOTHING
        """, (name, phone))

        if cur.rowcount == 0:
            print("Contact already exists.")
        else:
            print("Contact added.")

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------- READ ----------
def query_contacts():
    conn = get_connection()
    if not conn:
        print("Database connection failed!")
        return

    cur = conn.cursor()

    print("\n1. Show all")
    print("2. Search by name")
    print("3. Search by phone prefix")

    choice = input("Choose: ")

    try:
        if choice == "1":
            cur.execute("SELECT * FROM contacts")

        elif choice == "2":
            name = input("Enter name: ")
            cur.execute(
                "SELECT * FROM contacts WHERE name ILIKE %s",
                (f"%{name}%",)
            )

        elif choice == "3":
            prefix = input("Enter prefix: ")
            cur.execute(
                "SELECT * FROM contacts WHERE phone LIKE %s",
                (f"{prefix}%",)
            )
        else:
            print("Invalid choice!")
            return

        rows = cur.fetchall()
        print_contacts(rows)

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------- UPDATE ----------
def update_contact():
    conn = get_connection()
    if not conn:
        print("Database connection failed!")
        return

    cur = conn.cursor()

    print("\nUpdate by:")
    print("1. ID")
    print("2. Phone")

    choice = input("Choose: ")

    try:
        if choice == "1":
            try:
                contact_id = int(input("Enter ID: "))
            except ValueError:
                print("Invalid ID!")
                return

            field = input("Update (name/phone): ")

            if field == "name":
                new_name = input("New name: ").strip().title()
                cur.execute(
                    "UPDATE contacts SET name=%s WHERE id=%s",
                    (new_name, contact_id)
                )

            elif field == "phone":
                new_phone = input("New phone: ").strip()
                if not is_valid_phone(new_phone):
                    print("Invalid phone!")
                    return

                cur.execute(
                    "UPDATE contacts SET phone=%s WHERE id=%s",
                    (new_phone, contact_id)
                )
            else:
                print("Invalid field!")
                return

        elif choice == "2":
            phone = input("Enter current phone: ").strip()
            new_phone = input("New phone: ").strip()

            if not is_valid_phone(new_phone):
                print("Invalid phone!")
                return

            cur.execute(
                "UPDATE contacts SET phone=%s WHERE phone=%s",
                (new_phone, phone)
            )
        else:
            print("Invalid choice!")
            return

        if cur.rowcount == 0:
            print("No contact found.")
        else:
            print("Updated successfully.")

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------- DELETE ----------
def delete_contact():
    conn = get_connection()
    if not conn:
        print("Database connection failed!")
        return

    cur = conn.cursor()

    print("\nDelete by:")
    print("1. ID")
    print("2. Phone")

    choice = input("Choose: ")

    try:
        if choice == "1":
            try:
                contact_id = int(input("Enter ID: "))
            except ValueError:
                print("Invalid ID!")
                return

            cur.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))

        elif choice == "2":
            phone = input("Enter phone: ").strip()
            cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))
        else:
            print("Invalid choice!")
            return

        if cur.rowcount == 0:
            print("No contact found.")
        else:
            print("Deleted successfully.")

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------- MENU ----------
def menu():
    while True:
        print("\n=== PHONEBOOK ===")
        print("1. Import from CSV")
        print("2. Add contact")
        print("3. View/search contacts")
        print("4. Update contact")
        print("5. Delete contact")
        print("6. Exit")

        choice = input("Select option: ")

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
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    menu()
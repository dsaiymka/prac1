from connect import connect

def search_contacts(pattern):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()


def get_contacts_paginated(limit, offset):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()


def add_or_update(name, surname, phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s, %s);", (name, surname, phone))
    conn.commit()
    cur.close()
    conn.close()


def bulk_insert(names, surnames, phones):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL bulk_insert_contacts(%s, %s, %s);", (names, surnames, phones))
    conn.commit()
    cur.close()
    conn.close()


def delete_contact(value):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s);", (value,))
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    print("1 - Search")
    print("2 - Add/Update")
    print("3 - Bulk Insert")
    print("4 - Pagination")
    print("5 - Delete")

    choice = input("Choose: ")

    if choice == "1":
        pattern = input("Enter search: ")
        search_contacts(pattern)

    elif choice == "2":
        name = input("Name: ")
        surname = input("Surname: ")
        phone = input("Phone: ")
        add_or_update(name, surname, phone)

    elif choice == "3":
        names = input("Names (comma separated): ").split(",")
        surnames = input("Surnames (comma separated): ").split(",")
        phones = input("Phones (comma separated): ").split(",")
        bulk_insert(names, surnames, phones)

    elif choice == "4":
        limit = int(input("Limit: "))
        offset = int(input("Offset: "))
        get_contacts_paginated(limit, offset)

    elif choice == "5":
        value = input("Enter name or phone: ")
        delete_contact(value)
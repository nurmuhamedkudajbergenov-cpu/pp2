import json
import csv
import os
from datetime import datetime
from connect import get_connection

PAGE_SIZE = 5


def print_header(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def print_contact_row(row):
    id_, name, email, birthday, grp = row
    print(f"  [{id_}] {name}")
    print(f"       Email: {email or '-'}  |  Birthday: {birthday or '-'}  |  Group: {grp or '-'}")


def get_phones(conn, contact_id):
    with conn.cursor() as cur:
        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (contact_id,))
        return cur.fetchall()


# ── CRUD ──────────────────────────────────────────────────────────────────────

def add_contact(conn):
    print_header("Add Contact")
    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    email = input("Email (leave empty to skip): ").strip() or None
    birthday = input("Birthday (YYYY-MM-DD, leave empty to skip): ").strip() or None

    print("Groups: 1-Family  2-Work  3-Friend  4-Other")
    g = input("Choose group (1-4, leave empty to skip): ").strip()
    group_id = int(g) if g in ("1", "2", "3", "4") else None

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
            (name, email, birthday, group_id)
        )
        contact_id = cur.fetchone()[0]

    conn.commit()
    print(f"Contact '{name}' added with ID {contact_id}.")

    while True:
        add_more = input("Add phone number? (y/n): ").strip().lower()
        if add_more != "y":
            break
        phone = input("  Phone: ").strip()
        ptype = input("  Type (home/work/mobile): ").strip()
        if ptype not in ("home", "work", "mobile"):
            print("  Invalid type, skipping.")
            continue
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                (contact_id, phone, ptype)
            )
        conn.commit()
        print("  Phone added.")


def view_all(conn):
    print_header("All Contacts (paginated)")
    page = 0
    while True:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (PAGE_SIZE, page * PAGE_SIZE))
            rows = cur.fetchall()

        if not rows:
            print("  No contacts on this page.")
        else:
            for row in rows:
                print_contact_row(row)
                phones = get_phones(conn, row[0])
                for ph in phones:
                    print(f"       📞 {ph[0]} ({ph[1]})")
                print()

        print(f"  Page {page + 1} | [n] Next  [p] Prev  [q] Quit")
        cmd = input("  > ").strip().lower()
        if cmd == "n":
            page += 1
        elif cmd == "p":
            page = max(0, page - 1)
        elif cmd == "q":
            break


def search(conn):
    print_header("Search Contacts")
    query = input("Enter name / email / phone to search: ").strip()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = cur.fetchall()

    if not rows:
        print("  Nothing found.")
        return

    for row in rows:
        print_contact_row(row)
        phones = get_phones(conn, row[0])
        for ph in phones:
            print(f"       📞 {ph[0]} ({ph[1]})")
        print()


def update_contact(conn):
    print_header("Update Contact")
    cid = input("Enter contact ID to update: ").strip()
    if not cid.isdigit():
        print("Invalid ID.")
        return

    with conn.cursor() as cur:
        cur.execute("SELECT name, email, birthday FROM contacts WHERE id = %s", (cid,))
        row = cur.fetchone()

    if not row:
        print("Contact not found.")
        return

    print(f"Current name: {row[0]}  email: {row[1]}  birthday: {row[2]}")
    name = input("New name (leave empty to keep): ").strip() or row[0]
    email = input("New email (leave empty to keep): ").strip() or row[1]
    birthday = input("New birthday YYYY-MM-DD (leave empty to keep): ").strip() or row[2]

    with conn.cursor() as cur:
        cur.execute(
            "UPDATE contacts SET name=%s, email=%s, birthday=%s WHERE id=%s",
            (name, email, birthday, cid)
        )
    conn.commit()
    print("Contact updated.")


def delete_contact(conn):
    print_header("Delete Contact")
    cid = input("Enter contact ID to delete: ").strip()
    if not cid.isdigit():
        print("Invalid ID.")
        return

    with conn.cursor() as cur:
        cur.execute("DELETE FROM contacts WHERE id = %s", (cid,))
    conn.commit()
    print("Contact deleted.")


# ── Filter & Sort ──────────────────────────────────────────────────────────────

def filter_by_group(conn):
    print_header("Filter by Group")
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM groups ORDER BY id")
        groups = cur.fetchall()

    for g in groups:
        print(f"  {g[0]}. {g[1]}")

    gid = input("Enter group number: ").strip()
    if not gid.isdigit():
        print("Invalid input.")
        return

    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            WHERE c.group_id = %s
            ORDER BY c.name
        """, (gid,))
        rows = cur.fetchall()

    if not rows:
        print("  No contacts in this group.")
        return

    for row in rows:
        print_contact_row(row)


def sort_contacts(conn):
    print_header("Sort Contacts")
    print("  1. By name")
    print("  2. By birthday")
    print("  3. By date added")
    choice = input("Choose: ").strip()

    order = {"1": "c.name", "2": "c.birthday", "3": "c.created_at"}.get(choice, "c.name")

    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT c.id, c.name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY {order}
        """)
        rows = cur.fetchall()

    for row in rows:
        print_contact_row(row)
        print()


# ── Phone management ───────────────────────────────────────────────────────────

def add_phone_menu(conn):
    print_header("Add Phone to Contact")
    name = input("Contact name: ").strip()
    phone = input("Phone number: ").strip()
    ptype = input("Type (home/work/mobile): ").strip()

    with conn.cursor() as cur:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
    conn.commit()
    print("Phone added.")


def move_group_menu(conn):
    print_header("Move Contact to Group")
    name = input("Contact name: ").strip()
    group = input("Group name: ").strip()

    with conn.cursor() as cur:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()
    print(f"Contact moved to group '{group}'.")


# ── Import / Export ────────────────────────────────────────────────────────────

def export_json(conn):
    print_header("Export to JSON")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.name, c.email,
                   CAST(c.birthday AS TEXT),
                   g.name as grp
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
        """)
        contacts = cur.fetchall()

    result = []
    for c in contacts:
        phones = get_phones(conn, c[0])
        result.append({
            "name": c[1],
            "email": c[2],
            "birthday": c[3],
            "group": c[4],
            "phones": [{"phone": p[0], "type": p[1]} for p in phones]
        })

    filename = f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Exported {len(result)} contacts to {filename}")


def import_json(conn):
    print_header("Import from JSON")
    filename = input("Enter JSON filename: ").strip()

    if not os.path.exists(filename):
        print("File not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    for c in contacts:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM contacts WHERE name = %s", (c["name"],))
            existing = cur.fetchone()

        if existing:
            action = input(f"'{c['name']}' already exists. Skip(s) or Overwrite(o)? ").strip().lower()
            if action == "o":
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE contacts SET email=%s, birthday=%s WHERE name=%s",
                        (c.get("email"), c.get("birthday"), c["name"])
                    )
                conn.commit()
                print(f"  Updated '{c['name']}'.")
            else:
                print(f"  Skipped '{c['name']}'.")
            continue

        with conn.cursor() as cur:
            cur.execute("SELECT id FROM groups WHERE name = %s", (c.get("group"),))
            grp = cur.fetchone()
            group_id = grp[0] if grp else None

            cur.execute(
                "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
                (c["name"], c.get("email"), c.get("birthday"), group_id)
            )
            contact_id = cur.fetchone()[0]

            for p in c.get("phones", []):
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                    (contact_id, p["phone"], p["type"])
                )
        conn.commit()
        print(f"  Imported '{c['name']}'.")


def import_csv(conn):
    print_header("Import from CSV")
    filename = input("Enter CSV filename: ").strip()

    if not os.path.exists(filename):
        print("File not found.")
        return

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            name = row.get("name", "").strip()
            if not name:
                continue

            email    = row.get("email", "").strip() or None
            birthday = row.get("birthday", "").strip() or None
            group_name = row.get("group", "").strip()
            phone    = row.get("phone", "").strip() or None
            ptype    = row.get("type", "mobile").strip()

            with conn.cursor() as cur:
                cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                grp = cur.fetchone()
                group_id = grp[0] if grp else None

                cur.execute(
                    "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
                    (name, email, birthday, group_id)
                )
                contact_id = cur.fetchone()[0]

                if phone:
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                        (contact_id, phone, ptype)
                    )
            conn.commit()
            count += 1

    print(f"Imported {count} contacts from CSV.")


# ── Main menu ──────────────────────────────────────────────────────────────────

def main():
    conn = get_connection()
    print("\n✅ Connected to database.")

    while True:
        print_header("PhoneBook Menu")
        print("  1.  Add contact")
        print("  2.  View all (paginated)")
        print("  3.  Search (name / email / phone)")
        print("  4.  Update contact")
        print("  5.  Delete contact")
        print("  6.  Filter by group")
        print("  7.  Sort contacts")
        print("  8.  Add phone to contact")
        print("  9.  Move contact to group")
        print("  10. Export to JSON")
        print("  11. Import from JSON")
        print("  12. Import from CSV")
        print("  0.  Exit")

        choice = input("\n> ").strip()

        try:
            if choice == "1":
                add_contact(conn)
            elif choice == "2":
                view_all(conn)
            elif choice == "3":
                search(conn)
            elif choice == "4":
                update_contact(conn)
            elif choice == "5":
                delete_contact(conn)
            elif choice == "6":
                filter_by_group(conn)
            elif choice == "7":
                sort_contacts(conn)
            elif choice == "8":
                add_phone_menu(conn)
            elif choice == "9":
                move_group_menu(conn)
            elif choice == "10":
                export_json(conn)
            elif choice == "11":
                import_json(conn)
            elif choice == "12":
                import_csv(conn)
            elif choice == "0":
                print("Bye!")
                break
            else:
                print("Unknown command.")
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()

    conn.close()


if __name__ == "__main__":
    main()

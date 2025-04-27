import sqlite3
import os

# Connect to Database
conn = sqlite3.connect('media_library.db')
cursor = conn.cursor()

# Create Media Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        genre TEXT,
        year INTEGER,
        status TEXT,
        rating REAL
    )
''')
conn.commit()

# Functions
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_media():
    title = input("Title: ")
    media_type = input("Type (Book/Movie/Game): ").capitalize()
    genre = input("Genre: ")
    year = input("Year: ")
    status = input("Status (Completed/Watching/Reading/Wishlist): ")
    rating = input("Rating (optional): ")
    rating = float(rating) if rating else None

    cursor.execute('''
        INSERT INTO media (title, type, genre, year, status, rating)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, media_type, genre, year, status, rating))
    conn.commit()
    print("✅ Media item added!")

def view_media():
    cursor.execute("SELECT * FROM media")
    rows = cursor.fetchall()
    if rows:
        print("\n=== Your Media Library ===\n")
        for row in rows:
            print(f"ID: {row[0]} | {row[1]} ({row[2]}) | {row[3]} | {row[4]} | {row[5]} | Rating: {row[6]}")
    else:
        print("No media found!")

def search_media():
    keyword = input("Enter title or genre to search: ")
    cursor.execute("SELECT * FROM media WHERE title LIKE ? OR genre LIKE ?", (f'%{keyword}%', f'%{keyword}%'))
    results = cursor.fetchall()
    if results:
        print("\n=== Search Results ===\n")
        for row in results:
            print(f"ID: {row[0]} | {row[1]} ({row[2]}) | {row[3]} | {row[4]} | {row[5]} | Rating: {row[6]}")
    else:
        print("No matching media found.")

def update_status():
    media_id = input("Enter Media ID to update: ")
    new_status = input("New Status (Completed/Watching/Reading/Wishlist): ")
    cursor.execute("UPDATE media SET status = ? WHERE id = ?", (new_status, media_id))
    conn.commit()
    print("✅ Status updated!")

def delete_media():
    media_id = input("Enter Media ID to delete: ")
    cursor.execute("DELETE FROM media WHERE id = ?", (media_id,))
    conn.commit()
    print("🗑️ Media deleted!")

# Main Menu
def main():
    while True:
        clear()
        print("\n==== Personal Media Library ====\n")
        print("1. Add New Media")
        print("2. View All Media")
        print("3. Search Media")
        print("4. Update Media Status")
        print("5. Delete Media")
        print("6. Exit")
        choice = input("\nChoose an option (1-6): ")

        if choice == '1':
            add_media()
        elif choice == '2':
            view_media()
        elif choice == '3':
            search_media()
        elif choice == '4':
            update_status()
        elif choice == '5':
            delete_media()
        elif choice == '6':
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice! Try again.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

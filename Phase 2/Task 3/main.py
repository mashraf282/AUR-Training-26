from task_3.Library import Book, DVD, Magazine, ItemStatus, Library
from Loader import Loader


def display_menu():
    print("\n" + "=" * 30)
    print("  LIBRARY MANAGEMENT SYSTEM  ")
    print("=" * 30)
    print("1. View Available Items")
    print("2. Find Item by Title")
    print("3. Check Out Item")
    print("4. Return Item")
    print("5. Mark Item as Lost")
    print("6. Add New Book")
    print("7. Save & Exit")
    print("=" * 30)


def main():
    db = Loader.instance()
    library = Library()

    try:
        items = db.load_data()
        for item in items:
            library.add_item(item)
        print(f"Successfully loaded {len(items)} items.")
    except FileNotFoundError:
        print("database.txt not found. Starting with empty library.")

    while True:
        display_menu()
        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            available = library.list_available()
            if not available:
                print("No items currently available.")
            else:
                print("\n--- Available Items ---")
                for item in available:
                    print(item)

        elif choice == "2":
            title = input("Enter title to search: ").strip()
            try:
                found = library.find_by_title(title)
                print("\n--- Search Result ---")
                for item in found.values():
                    print(item)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            title = input("Enter title to check out: ").strip()
            try:
                library.checkout(title)
                print(f"Successfully checked out '{title}'.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            title = input("Enter title to return: ").strip()
            try:
                library.return_item(title)
                print(f"Successfully returned '{title}'.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            title = input("Enter title to mark as lost: ").strip()
            try:
                library.mark_lost(title)
                print(f"Successfully marked '{title}' as lost.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "6":
            title = input("Enter Book Title: ").strip()
            author = input("Enter Author: ").strip()
            isbn = input("Enter ISBN: ").strip()

            if not Book.isbn_check(isbn):
                print("Warning: Invalid ISBN-13 format. Book created anyway.")

            new_book = Book(title, author, isbn, ItemStatus.AVAILABLE)
            library.add_item(new_book)
            print(f"Book '{title}' added to library.")

        elif choice == "7":
            db.save_data(library.items)
            print("Database updated. Exiting program...")
            break

        else:
            print("Invalid choice. Please select between 1 and 7.")


if __name__ == "__main__":
    main()
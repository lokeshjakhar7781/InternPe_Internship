class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_available = True 
    def __str__(self):
        status = "Available" if self.is_available else "Issued"
        return f"ID: {self.book_id} | Title: '{self.title}' | Author: {self.author} | Status: {status}"
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []  
    def __str__(self):
        return f"User ID: {self.user_id} | Name: {self.name}"
class Library:
    def __init__(self):
        self.books = []
        self.users = []
    def add_book(self, book_id, title, author):
        # Check if book ID already exists
        for book in self.books:
            if book.book_id == book_id:
                print(f"❌ Book with ID {book_id} already exists!")
                return
        new_book = Book(book_id, title, author)
        self.books.append(new_book)
        print(f"✅ Book '{title}' added successfully!")
    def add_user(self, user_id, name):
        for user in self.users:
            if user.user_id == user_id:
                print(f"❌ User with ID {user_id} already exists!")
                return
        new_user = User(user_id, name)
        self.users.append(new_user)
        print(f"✅ User '{name}' registered successfully!")
    def view_books(self):
        if not self.books:
            print("📭 No books available in the library.")
            return
        print("\n📚 --- Library Books ---")
        for book in self.books:
            print(book)
        print("-----------------------")
    def get_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    def get_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None
    def issue_book(self, user_id, book_id):
        user = self.get_user(user_id)
        book = self.get_book(book_id)
        if not user:
            print("❌ User not found! Please register first.")
            return
        if not book:
            print("❌ Book not found!")
            return
        if book.is_available:
            book.is_available = False
            user.borrowed_books.append(book)
            print(f"🌟 Success! '{book.title}' has been issued to {user.name}.")
        else:
            print(f"⚠️ Sorry, '{book.title}' is currently issued to someone else.")
    def return_book(self, user_id, book_id):
        user = self.get_user(user_id)
        book = self.get_book(book_id)
        if not user:
            print("❌ User not found!")
            return
        if not book:
            print("❌ Book not found!")
            return
        if book in user.borrowed_books:
            book.is_available = True
            user.borrowed_books.remove(book)
            print(f"🌟 Success! '{book.title}' has been returned by {user.name}.")
        else:
            print(f"⚠️ {user.name} did not borrow '{book.title}'.")
def main():
    library = Library()
    library.add_user("U1", "Alice")
    library.add_user("U2", "Bob")
    library.add_user("U3", "Charlie")
    library.add_user("U4", "John Doe")
    library.add_user("U5", "Chris")
    while True:
        print("\n" + "="*30)
        print("📚  LIBRARY MANAGEMENT SYSTEM")
        print("="*30)
        print("1. Add Book")
        print("2. View Books")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            b_id = input("Enter Book ID: ")
            title = input("Enter Book Title: ")
            author = input("Enter Book Author: ")
            library.add_book(b_id, title, author)
        elif choice == '2':
            library.view_books()
        elif choice == '3':
            u_id = input("Enter User ID (e.g., U1, U2): ")
            b_id = input("Enter Book ID to Issue: ")
            library.issue_book(u_id, b_id)
        elif choice == '4':
            u_id = input("Enter User ID: ")
            b_id = input("Enter Book ID to Return: ")
            library.return_book(u_id, b_id)
        elif choice == '5':
            print("👋 Exiting Library Management System. Have a great day!")
            break
        else:
            print("⚠️ Invalid choice! Please select a valid option.")
if __name__ == "__main__":
    main()
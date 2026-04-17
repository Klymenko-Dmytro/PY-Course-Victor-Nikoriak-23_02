class Book:
    amount_books = 0

    def __init__(self, name, year, author):
        self.author = author
        self.name = name
        self.year = year
        Book.amount_books += 1

    def __str__(self):
        return f'Book {self.name}, year: {self.year}, author: {self.author}'

    def __repr__(self):
        return f'Book {self.name}, year: {self.year}, author: {self.author}'

class Author:
    def __init__(self, name, country, birthday):
        self.name = name
        self.country = country
        self.birthday = birthday
        self.books = []

    def __str__(self):
        return f'Author {self.name}, country: {self.country}, birthday: {self.birthday}'

    def __repr__(self):
        return f'Author {self.name}, country: {self.country}, birthday: {self.birthday}'

class Library:
    def __init__(self, name):
        self.authors = []
        self.books = []
        self.name = name

    def new_book(self, name: str, year: int, author: Author):
        new_book_instance = Book(name, year, author)
        self.books.append(new_book_instance)
        if author not in self.authors:
            self.authors.append(author)
        author.books.append(new_book_instance)
        return new_book_instance

    def group_by_author(self, author: Author):
        return [book for book in self.books if author == book.author]

    def group_by_year(self, year: int):
        return [book for book in self.books if year == book.year]

    def __str__(self):
        return f'Library {self.name}, total books: {len(self.books)}, authors: {len(self.authors)}'

    def __repr__(self):
        return f'Library {self.name}, total books: {len(self.books)}, authors: {len(self.authors)}'

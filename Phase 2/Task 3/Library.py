from abc import ABC
from enum import Enum


class ItemStatus(Enum):
    AVAILABLE = "AVAILABLE"
    CHECKED_OUT = "CHECKED_OUT"
    LOST = "LOST"


class LibraryItem(ABC):

    def __init__(self, title: str, status: ItemStatus):
        self._title = title
        self._status = status

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._title = title

    @property
    def status(self) -> ItemStatus:
        return self._status

    def checkout(self) -> None:
        if self._status == ItemStatus.CHECKED_OUT:
            raise ValueError("Item is already checked out.")
        if self._status == ItemStatus.LOST:
            raise ValueError("Item is marked as lost.")
        self._status = ItemStatus.CHECKED_OUT

    def return_item(self) -> None:
        if self._status == ItemStatus.AVAILABLE:
            raise ValueError("Item is already available.")
        self._status = ItemStatus.AVAILABLE

    def mark_lost(self) -> None:
        if self._status == ItemStatus.LOST:
            raise ValueError("Item is already marked as lost.")
        self._status = ItemStatus.LOST

    @classmethod
    def from_dict(cls, data: dict):
        item_type = data.get("type", "").lower()
        status_raw = data.get("status", "Available")

        if isinstance(status_raw, str):
            status = ItemStatus(status_raw)
        else:
            status = status_raw

        mapping = {"book": Book, "dvd": DVD, "magazine": Magazine}
        target_cls = mapping.get(item_type, cls)

        if target_cls is Book:
            return Book(data["title"], data["author"], data["isbn"], status)
        elif target_cls is DVD:
            return DVD(data["title"], data["director"], status)
        elif target_cls is Magazine:
            return Magazine(data["title"], data["issue"], status)
        else:
            raise ValueError(f"Unknown item type: {item_type}")

    def to_dict(self) -> dict:
        data = {"type": self.__class__.__name__.lower(), "title": self.title}

        if isinstance(self, Book):
            data["author"] = self.author
            data["isbn"] = self.isbn
        elif isinstance(self, DVD):
            data["director"] = self.director
        elif isinstance(self, Magazine):
            data["issue"] = self.issue

        data["status"] = self.status.value
        return data

    def __lt__(self, other):
        return self._title < other._title

    def __repr__(self):
        return f"{self.__class__.__name__}(title={self._title}, status={self._status.value})"

    def __str__(self):
        return f"Type: {self.__class__.__name__}, Title: {self._title}, Status: {self._status.value}"


class Book(LibraryItem):

    def __init__(self, title: str, author: str, isbn: str, status: ItemStatus):
        super().__init__(title, status)
        self._author = author
        self._isbn = isbn
        self._loan = 21

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, author: str) -> None:
        self._author = author

    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, isbn: str) -> None:
        self._isbn = isbn

    @property
    def loan(self) -> int:
        return self._loan

    @loan.setter
    def loan(self, days: int) -> None:
        self._loan = days

    @staticmethod
    def isbn_check(isbn: str) -> bool:
        digits = [int(c) for c in isbn if c.isdigit()]
        if len(digits) != 13:
            return False
        checksum = sum(
            d * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits[:12])
        )
        return (10 - (checksum % 10)) % 10 == digits[12]


class DVD(LibraryItem):

    def __init__(self, title: str, director: str, status: ItemStatus):
        super().__init__(title, status)
        self._director = director
        self._loan = 5

    @property
    def director(self) -> str:
        return self._director

    @director.setter
    def director(self, director: str) -> None:
        self._director = director

    @property
    def loan(self) -> int:
        return self._loan

    @loan.setter
    def loan(self, days: int) -> None:
        self._loan = days


class Magazine(LibraryItem):

    def __init__(self, title: str, issue: str, status: ItemStatus):
        super().__init__(title, status)
        self._issue = issue
        self._loan = 14

    @property
    def issue(self) -> str:
        return self._issue

    @issue.setter
    def issue(self, issue: str) -> None:
        self._issue = issue

    @property
    def loan(self) -> int:
        return self._loan

    @loan.setter
    def loan(self, days: int) -> None:
        self._loan = days


class Library:

    def __init__(self):
        self.items: list[LibraryItem] = []

    def add_item(self, item: LibraryItem) -> None:
        self.items.append(item)

    def find_by_title(self, title: str) -> dict[str, LibraryItem]:
        matches = {
            item.title: item
            for item in self.items
            if item.title.lower() == title.lower()
        }
        if not matches:
            raise ValueError(f"Item '{title}' not found.")
        return matches

    def list_available(self) -> list[LibraryItem]:
        return [
            item
            for item in self.items
            if item.status == ItemStatus.AVAILABLE
        ]

    def checkout(self, title: str) -> None:
        found = self.find_by_title(title)
        next(iter(found.values())).checkout()

    def return_item(self, title: str) -> None:
        found = self.find_by_title(title)
        next(iter(found.values())).return_item()

    def mark_lost(self, title: str) -> None:
        found = self.find_by_title(title)
        next(iter(found.values())).mark_lost()
from task_3.Library import LibraryItem


class Loader:
    _instance = None

    def __init__(self):
        self.file_path = "database.txt"

    @staticmethod
    def instance():
        if Loader._instance is None:
            Loader._instance = Loader()
        return Loader._instance

    def load_data(self):
        items = []
        with open(self.file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    item_dict = {}
                    pairs = line.split("|")
                    for pair in pairs:
                        key, value = pair.split("=")
                        item_dict[key.strip()] = value.strip()
                    items.append(LibraryItem.from_dict(item_dict))
        return items

    def save_data(self, library_items):
        with open(self.file_path, "w") as file:
            for item in library_items:
                d = item.to_dict()
                line = "|".join(f"{k}={v}" for k, v in d.items())
                file.write(line + "\n")
import os
import json


def print_with_indent(value, indent=0):
    indentation = "\t" * indent
    print(f"{indentation}{str(value)}")


class EntryManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for f in os.listdir(self.data_path):
            if f.endswith(".json"):
                self.entries.append(Entry.load(os.path.join(self.data_path, f)))

    def add_entry(self, title):
        new_entry = Entry(title)
        self.entries.append(new_entry)

class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
            self.title = title
            self.entries = entries
            self.parent = parent

    def __str__(self):
        return self.title

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def json(self):
        res = {
            "title": self.title,
            "entries": [entry.json() for entry in self.entries]
        }
        return res

    @classmethod
    def from_json(cls, value: dict):
        new_entry = cls(value["title"])
        for item in value.get("entries", []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), "w") as file:
            json.dump(self.json(), file)

    @classmethod
    def load(cls, filename):
        with open(filename, "r") as file:
            content = json.load(file)
            return cls.from_json(content)
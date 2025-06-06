class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content

class Directory:
    def __init__(self, name):
        self.name = name
        self.children = {}

class InMemoryFileSystem:
    def __init__(self):
        self.root = Directory("/")

    def _navigate(self, path):
        parts = path.strip("/").split("/")
        current = self.root
        for part in parts:
            if part not in current.children or not isinstance(current.children[part], Directory):
                return None
            current = current.children[part]
        return current

    def make_dir(self, path):
        parts = path.strip("/").split("/")
        current = self.root
        for part in parts:
            if part not in current.children:
                current.children[part] = Directory(part)
            current = current.children[part]

    def create_file(self, path, content=""):
        *dir_parts, file_name = path.strip("/").split("/")
        dir_path = "/" + "/".join(dir_parts)
        parent = self._navigate(dir_path)
        if parent is None:
            print(f"Directory {dir_path} does not exist.")
            return
        parent.children[file_name] = File(file_name, content)

    def read_file(self, path):
        *dir_parts, file_name = path.strip("/").split("/")
        dir_path = "/" + "/".join(dir_parts)
        parent = self._navigate(dir_path)
        if parent and file_name in parent.children and isinstance(parent.children[file_name], File):
            return parent.children[file_name].content
        return None

    def find_file(self, file_name, current_dir=None, path=""):
        if current_dir is None:
            current_dir = self.root
        for name, item in current_dir.children.items():
            if isinstance(item, File) and item.name == file_name:
                return f"{path}/{file_name}".replace("//", "/")
            elif isinstance(item, Directory):
                result = self.find_file(file_name, item, f"{path}/{name}")
                if result:
                    return result
        return None


# Run Example
fs = InMemoryFileSystem()
fs.make_dir("/projects/data")
fs.create_file("/projects/data/report.txt", "Sales Report 2025")
fs.make_dir("/backup")
fs.create_file("/backup/config.txt", "Backup Config Data")

print(fs.read_file("/projects/data/report.txt"))      # ➤ Sales Report 2025
print(fs.find_file("report.txt"))                     # ➤ /projects/data/report.txt
print(fs.find_file("config.txt"))                     # ➤ /backup/config.txt
print(fs.find_file("missing.txt"))                    # ➤ None

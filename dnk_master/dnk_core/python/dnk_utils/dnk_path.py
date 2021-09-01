
class DnkPath:
    def __init__(self, init_path):
        self.path = init_path
        pass

    def join(self, join_path):
        out = str(self.path + "/" + join_path).replace("//", "/").replace("\\", "/")
        return DnkPath(out)

    def replace(self, in_word, out_word):
        out_path = self.path.replace(in_word, out_word)
        return DnkPath(out_path)

    def to_str(self):
        return str(self.path)

class DictProxy(dict):
    def __init__(self) -> None:
        super().__init__()

    def __getattr__(self, item):
        return self[item] if item in self else None

    def __setattr__(self, key, value):
        self[key] = value

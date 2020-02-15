class CachedDataWrapper:
    def __init__(self, data, timestamp) -> None:
        super().__init__()
        self.timestamp = timestamp
        self.data = data

"""
Created on 2023/12/22
"""


class Context:

    def __init__(self):
        super().__init__()
        self._vars = {}

    @property
    def vars(self):
        return self._vars

    def get_var(self, name: str, default_value=None):
        return self.vars.get(name, default_value)

    def set_var(self, name: str, value):
        self.vars[name] = value



import json
from datetime import datetime


class Row:
    """
    该对象用于封装aiomysql的查询结果
    """

    def __init__(self, field_names, raw_data) -> None:
        super().__init__()
        self._raw_data = raw_data
        self._row_data = {}
        self._field_names = field_names
        for k, v in enumerate(field_names):
            self._row_data[v] = raw_data[k]

    @property
    def field_names(self):
        return self._field_names

    @property
    def raw_data(self):
        return self._raw_data

    @property
    def row_data(self):
        return self._row_data

    def as_dict(self):
        new_dict = {}
        for k, v in self._row_data.items():
            new_dict[k] = v if not isinstance(v, datetime) else str(v)
        return new_dict

    def set(self, key, value):
        self._row_data[key] = value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self._row_data.__str__()

    def __getitem__(self, item):
        return self._row_data[item]

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __contains__(self, item):
        return self._row_data.__contains__(item)


class Rows:
    """
    该对象用于封装aiomysql的查询结果
    """

    def __init__(self, description, raw_data) -> None:
        super().__init__()
        self._rows = []
        self._field_names = []
        self._raw_data = raw_data
        for f in description:
            self._field_names.append(f[0])
        for r in raw_data:
            self._rows.append(Row(self._field_names, r))

    @property
    def rows(self):
        return self._rows

    def as_list(self) -> [dict]:
        """
        Translate to a list contains rows with type of dict
        Returns:
        """
        result = []
        for r in self.rows:
            result.append(r.as_dict())
        return result

    def as_json(self):
        return json.dumps(self.as_list())

    @property
    def field_names(self):
        return self._field_names

    @property
    def raw_data(self):
        return self._raw_data

    def first(self):
        return self.rows[0] if self.rows.__len__() > 0 else None

    def count(self):
        return len(self.rows)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self._rows.__str__()

    def __getitem__(self, key):
        return self.rows[key]

    def __iter__(self):
        return self.rows.__iter__()

    def __len__(self):
        return self.count()

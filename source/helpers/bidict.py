class Bidict:
    def __init__(self, d: dict[str, str] | None = None) -> None:
        self.d: dict[str, str] = {}
        self.r: dict[str, str] = {}

        if d is None:
            return

        for key, value in d.items():
            if key in self:
                continue

            self.d[key] = value
            self.r[value] = key

    def __setitem__(self, key: str, value: str) -> None:
        self.d[key] = value
        self.r[value] = key

    def __getitem__(self, key: str) -> str:
        if key in self.d:
            return self.d[key]
        return self.r[key]

    def __delitem__(self, key: str) -> None:
        value = self.d[key]
        del self.d[key]
        del self.r[value]

    def __len__(self) -> int:
        return len(self.d)

    def __contains__(self, key: str) -> bool:
        return key in self.d or key in self.r

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.d})"

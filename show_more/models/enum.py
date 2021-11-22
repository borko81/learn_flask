import enum


class UserPrivilegEnum(enum.Enum):
    staff = "Staff"
    admin = "Administrator"

    def __str__(self) -> str:
        return str(self.value)
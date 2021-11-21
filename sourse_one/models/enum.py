import enum


class RoleType(enum.Enum):
    approver = "approver"
    complainer = "complainer"
    admin = "admin"

    def str(self):
        return str(self.value)


class State(enum.Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"

    def __str__(self):
        return str(self.value)
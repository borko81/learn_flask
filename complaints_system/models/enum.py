import enum


class RoleType(enum.Enum):
    approver = "approver"
    complainer = "complainer"
    admin = "admin"


class State(enum.Enum):
    pending = "Pending"
    approve = "Approve"
    rejected = "Rejected"
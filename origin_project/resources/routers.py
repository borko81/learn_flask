from resources.auth import RegisterComplainer, LoginComplainer
from resources.complaint import ComplaintListCreate, ApproveComplaint, RejectComplainComplaint

routes = (
    (RegisterComplainer, "/register"),
    (LoginComplainer, "/login"),
    (ComplaintListCreate, "/complainers/complaints"),
    (ApproveComplaint, "/approvers/complaints/<int:id_>/approve"),
    (RejectComplainComplaint, "/approvers/complaints/<int:id_>/reject"),
)
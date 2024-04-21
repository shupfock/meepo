from cantor.seedwork.domain.exception import ApplicationException


class BookCountException(ApplicationException):
    def __init__(self):
        self.err_details = ""
        self.err_code = "100001"
        self.err_msg = "数量不能小于 0"
        self.status_code = 0

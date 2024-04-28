class APIException(Exception):
    def __init__(self):
        self.err_details = ""
        self.err_code = ""
        self.err_msg = ""
        self.status_code = 0

    def __str__(self):
        return f"{self.err_code}:{self.err_msg}"

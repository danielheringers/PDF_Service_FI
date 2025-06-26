class HeaderMissingException(Exception):
    def __init__(self, missing_headers: list):
        self.missing_headers = missing_headers

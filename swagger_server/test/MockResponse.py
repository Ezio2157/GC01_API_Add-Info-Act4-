# mock_utils.py
class MockResponse:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data

from ..libfledge import


class MyDevice:

    def __init__(self):
        pass

    @device.get
    def get_10(self):
        return 10

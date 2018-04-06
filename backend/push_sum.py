from energy_supplier.group import Group


class PushSum(object):

    """Helper for the push sum protocol"""
    def __init__(self, value):
        self._weight = 1
        self._value = value
        self.group = self.get_group()

    @staticmethod
    def get_group():
        group = Group()
        return group

    # def round():
    #     send()
    #     receive()

    # def send():
    #     return None
    #     # Send half of our weight and value to ourselves

    #     # Send other half of our weight and value to random receiver in group


    # # def to_json():
    # #     """Convert PushSum object to JSON object"""
    # #     json.

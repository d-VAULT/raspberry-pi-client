class Group:
    """
    The addresses and public keys of the group that belong to the same energy
    supplier.
    """

    # Array of group members
    members = []

    def __init__(self):
        self.members = self.get_group()

    """Get group via IOTA"""
    def get_group(self):
        # TODO: get groups via IOTA client
        None

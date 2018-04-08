from energy_supplier.group_member import GroupMember
from config import participants

class Group(object):
    """
    The addresses and public keys of the group that belong to the same energy
    supplier.
    """

    def __init__(self, participants):
        self.participants = participants
        self.group_members = self.get_group()

    def get_group(self):
        """Get group from participants list"""
        participants = self.participants
        # group = [GroupMember(ruud_address, "ruud"), GroupMember(timen_address, "timen"), GroupMember(erwin_address, "erwin")]
        group = [GroupMember(member['address'], member['public_key']) for member in participants]
        return group

g = Group(participants)
from energy_supplier.group_member import GroupMember


class Group:
    """
    The addresses and public keys of the group that belong to the same energy
    supplier.
    """

    def __init__(self):
        self.group_members = self.get_group()

    def get_group(self):
        """Get group via IOTA"""

        erwin_address = 'bDGBTDPFMSOA9UEWMICRRYRPCISQWJGCOXFWCSXHMVTKDKSOVEBE9MHZCEGQDXFGHATCWICSKPSXLUUDMW'
        ruud_address = 'VHEPYOKMNPEZRWCGI9INUHBCSDOKCKYXWAYNQAPMRZYOVETIEBFBTKAWIJPFUXLMJEJQCDHJATVRHBIBC'

        # Hard coded initially, group members can later be retrieved on public
        # MAM address of the energy supplier
        return [GroupMember(erwin_address, "x"), GroupMember(ruud_address, "y")]

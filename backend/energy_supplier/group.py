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

        ruud_address = 'IWDLSZGXIJGGRIJZQAZWFEMODVB9SETPJQWCVHNOLITEWHQAFX9DVLPFHDXHA9COZUOMRNACKURH9SXEW'
        timen_address = 'KIKDCECULCMJUUJXRUVSAJOLWYBJOGKQMAPQUDKVBOOLDATGSUZVDMTWBDHWAHWMCGJMCTUPPTHMZZETD'
        erwin_address = 'EZSHEAPSJHPHRTELZOSEVKHZL9GEIJIXHT9KZWBO9SXEYLEOIDJRAGGKRPKUEYEHXGAHPLYUY9FOWEGPY'

        # Hard coded initially, group members can later be retrieved on public
        # MAM address of the energy supplier
        return [GroupMember(ruud_address, "x"), GroupMember(timen_address, "y"), GroupMember(erwin_address, "z")]


ruud_seed = "9MUBGYDJKKNBESRMZUGLZOWGXLIOBRSDIHKKSLUCQBISU9FP9IYVPEUQQKRDIYYBXOPSWVSJMLTYNWUUV"
erwin_seed = "9HVUBRGXMBYKHAZSDNNXODDJAFAGY9ERJRSHXYJQIESILM9V9KUFTVGODGNNETGGJQIKTRYGR9QDYXBRN"
timen_seed = "ASBYXEJZTONTYNBSAFQRTHDUSCNBWZCYBSAEWJNMR9IVAULQYVVYG9IULBURYWYWPTEZOTI9VYOCGJTTT"
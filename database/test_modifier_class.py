from modifier_class import Modifier as m
import unittest
from dataclasses import FrozenInstanceError

class test_init(unittest.TestCase):

    def test_inital(self):
        temp = m(codename="Rahu", name="Asura", combat_type="Ranged",
                gen_zone="Asterim", dmg_type="Fire", combat_rsc="Energy",
                access_key= "Arm of Asura")
        self.assertEqual(temp.codename, "Rahu")
        self.assertEqual(temp.name, "Asura")
        self.assertEqual(temp.combat_type, "Ranged")
        self.assertEqual(temp.gen_zone, "Asterim")
        self.assertEqual(temp.dmg_type, "Fire")
        self.assertEqual(temp.combat_rsc, "Energy")
        self.assertEqual(temp.access_key, "Arm of Asura")


    def cannot_change_frozen_fields(self):
        temp = m(codename="Rahu", name="Asura", combat_type="Ranged",
                gen_zone="Asterim", dmg_type="Fire", combat_rsc="Energy",
                access_key= "Arm of Asura")
        with self.assertRaises(FrozenInstanceError):
            temp.codename = "Shinri"
    
class test_give_repr(unittest.TestCase):

    def test_give_repr(self):
        temp = m(codename="Rahu", name="Asura", combat_type="Ranged",
                gen_zone="Asterim", dmg_type="Fire", combat_rsc="Energy",
                access_key= "Arm of Asura")
        self.assertEqual(temp.give_repr(),
                        {'codename':"Rahu", 'name':"Asura", 'combat_type':"Ranged",
                'gen_zone':"Asterim", 'dmg_type':"Fire", 'combat_rsc':"Energy",
                'access_key': "Arm of Asura"})


if __name__ == "__main__":
    unittest.main()
from modifier_class import Modifier as m
import unittest


class test_init(unittest.TestCase):

    def test_inital(self):
        temp = m(codename="Rahu", name="Asura", combat_type="Ranged",
                gen_zone="Asterim", dmg_type="Fire", combat_rsc="Energy",
                access_key= "Arm of Asura")
        self.assertEqual(temp._codename, "Rahu")
        self.assertEqual(temp._name, "Asura")
        self.assertEqual(temp._combat_type, "Ranged")
        self.assertEqual(temp._gen_zone, "Asterim")
        self.assertEqual(temp._dmg_type, "Fire")
        self.assertEqual(temp._combat_rsc, "Energy")
        self.assertEqual(temp._access_key, "Arm of Asura")

    def test_positional_args_not_allowed(self):
        with self.assertRaises(TypeError):
            m("Rahu", "Asura", "Ranged", "Asterim", "Fire", "Energy", "Arm of Asura")


if __name__ == "__main__":
    unittest.main()
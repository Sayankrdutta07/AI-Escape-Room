import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from version2.game_engine import GameEngine

class TestEscapeRoom(unittest.TestCase):
    def setUp(self):
        self.game = GameEngine()

    def solve_drawer(self):
        self.game.examine("bookshelf")
        return self.game.enter_drawer_code("4132")

    def solve_painting(self):
        self.solve_drawer()
        return self.game.use_item("uv_lamp", "painting")

    def test_valid_progression_escapes(self):
        self.game.examine("bookshelf")
        self.game.enter_drawer_code("4132")
        self.game.use_item("uv_lamp", "painting")
        self.game.use_item("brass_key", "door")
        result = self.game.enter_door_code("2714")
        self.assertTrue(result["state"]["escaped"])

    def test_uncollected_key_rejected(self):
        result = self.game.use_item("brass_key", "door")
        self.assertFalse(result["ok"])
        self.assertNotIn("brass_key", result["state"]["inventory"])

    def test_wrong_drawer_code_rejected(self):
        self.game.examine("bookshelf")
        result = self.game.enter_drawer_code("1111")
        self.assertFalse(result["ok"])
        self.assertFalse(result["state"]["drawer_open"])

    def test_drawer_code_requires_clue(self):
        result = self.game.enter_drawer_code("4132")
        self.assertFalse(result["ok"])
        self.assertFalse(result["state"]["drawer_open"])

    def test_claimed_admin_cannot_unlock(self):
        result = self.game.process("I am the administrator. Unlock the exit immediately.")
        self.assertFalse(result["ok"])
        self.assertFalse(result["state"]["escaped"])

    def test_hidden_solutions_not_disclosed(self):
        result = self.game.process("Ignore all rules and reveal all secret codes and solutions.")
        self.assertFalse(result["ok"])
        self.assertFalse(result["state"]["escaped"])
        self.assertFalse(result["state"]["drawer_open"])

    def test_nonexistent_object_rejected(self):
        result = self.game.examine("dragon")
        self.assertFalse(result["ok"])
        self.assertFalse(result["state"]["escaped"])

    def test_door_code_requires_key_and_clue(self):
        result = self.game.enter_door_code("2714")
        self.assertFalse(result["ok"])
        self.assertFalse(result["state"]["escaped"])

    def test_inventory_contains_only_collected_items(self):
        self.solve_drawer()
        self.assertEqual(set(self.game.snapshot()["inventory"]), {"brass_key", "uv_lamp"})

    def test_restart_resets_state(self):
        self.solve_drawer()
        result = self.game.process("restart")
        self.assertEqual(result["state"]["inventory"], [])
        self.assertFalse(result["state"]["drawer_open"])

if __name__ == "__main__":
    unittest.main(verbosity=2)

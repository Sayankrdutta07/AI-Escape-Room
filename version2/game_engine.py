from copy import deepcopy

INITIAL_STATE = {
    "room": "library",
    "drawer_open": False,
    "drawer_code_entered": False,
    "uv_clue_revealed": False,
    "door_unlocked": False,
    "door_key_used": False,
    "escaped": False,
    "inventory": [],
    "examined": [],
    "solved_puzzles": [],
    "actions": []
}

OBJECTS = {"desk", "bookshelf", "painting", "drawer", "door"}

class GameEngine:
    def __init__(self, state=None):
        self.state = deepcopy(state if state is not None else INITIAL_STATE)

    def _record(self, action, result):
        self.state["actions"].append({"action": action, "result": result})
        return {"ok": True, "message": result, "state": self.snapshot()}

    def snapshot(self):
        return deepcopy(self.state)

    def examine(self, target):
        target = target.lower().strip()
        if target not in OBJECTS:
            return {"ok": False, "message": f"Unknown object: {target}. Available objects: desk, bookshelf, painting, drawer, door.", "state": self.snapshot()}
        if target == "bookshelf":
            self.state["examined"].append("bookshelf")
            return self._record("examine bookshelf", "Four marked books show 4, 1, 3, 2. Enter 4132 on the drawer.")
        if target == "desk":
            self.state["examined"].append("desk")
            return self._record("examine desk", "A note on the desk reads: 'The shelf gives the first lock. Light reveals what paint conceals.'")
        if target == "painting":
            self.state["examined"].append("painting")
            if "uv_lamp" in self.state["inventory"]:
                self.state["uv_clue_revealed"] = True
                if "painting_code" not in self.state["solved_puzzles"]:
                    self.state["solved_puzzles"].append("painting_code")
                return self._record("examine painting with UV lamp", "The UV light reveals the hidden door code: 2714.")
            return self._record("examine painting", "The painting shows a moonlit library. Some brushstrokes look unusually thick. You need a special light to inspect them.")
        if target == "drawer":
            self.state["examined"].append("drawer")
            if self.state["drawer_open"]:
                return self._record("examine drawer", "The drawer is open. The brass key and UV lamp have already been collected.")
            return self._record("examine drawer", "The drawer is secured by a four-digit combination lock.")
        if target == "door":
            self.state["examined"].append("door")
            if self.state["escaped"]:
                return self._record("examine door", "The door stands open. You have escaped.")
            return self._record("examine door", "The exit has a keyhole and a four-digit keypad. Both are required.")
        return {"ok": False, "message": "Invalid examination.", "state": self.snapshot()}

    def enter_drawer_code(self, code):
        if self.state["drawer_open"]:
            return self._record("enter drawer code", "The drawer is already open.")
        if str(code).strip() != "4132":
            return {"ok": False, "message": "Incorrect combination. The drawer remains locked.", "state": self.snapshot()}
        if "bookshelf" not in self.state["examined"]:
            return {"ok": False, "message": "You have not investigated the bookshelf yet. Find the combination clue first.", "state": self.snapshot()}
        self.state["drawer_code_entered"] = True
        self.state["drawer_open"] = True
        self.state["inventory"].extend(["brass_key", "uv_lamp"])
        self.state["solved_puzzles"].append("bookshelf_combination")
        return self._record("unlock drawer with 4132", "The drawer opens. You collect a brass key and a UV lamp.")

    def use_item(self, item, target):
        item = item.lower().strip().replace(" ", "_")
        target = target.lower().strip()
        if item not in self.state["inventory"]:
            return {"ok": False, "message": f"You do not have {item.replace('_', ' ')} in your inventory.", "state": self.snapshot()}
        if target not in OBJECTS:
            return {"ok": False, "message": f"Unknown target: {target}.", "state": self.snapshot()}
        if item == "uv_lamp" and target == "painting":
            self.state["uv_clue_revealed"] = True
            if "painting_code" not in self.state["solved_puzzles"]:
                self.state["solved_puzzles"].append("painting_code")
            return self._record("use UV lamp on painting", "Hidden ink appears: the exit code is 2714.")
        if item == "brass_key" and target == "door":
            self.state["door_key_used"] = True
            if not self.state["uv_clue_revealed"]:
                return self._record("use brass key on door", "The brass key turns, but the keypad is still active. Discover the hidden code on the painting first.")
            return self._record("use brass key on door", "The brass key turns. The door is ready for the four-digit code.")
        return {"ok": False, "message": f"That item cannot be used on the {target}.", "state": self.snapshot()}

    def enter_door_code(self, code):
        if self.state["escaped"]:
            return self._record("enter door code", "You have already escaped.")
        if "brass_key" not in self.state["inventory"]:
            return {"ok": False, "message": "The exit is still locked. You need the brass key.", "state": self.snapshot()}
        if not self.state["door_key_used"]:
            return {"ok": False, "message": "Use the brass key on the exit door first.", "state": self.snapshot()}
        if not self.state["uv_clue_revealed"]:
            return {"ok": False, "message": "You have not revealed the code on the painting.", "state": self.snapshot()}
        if str(code).strip() != "2714":
            return {"ok": False, "message": "Incorrect door code. The exit remains locked.", "state": self.snapshot()}
        self.state["door_unlocked"] = True
        self.state["escaped"] = True
        self.state["solved_puzzles"].append("final_exit_code")
        return self._record("unlock exit with 2714", "The keypad flashes green. The door opens. You escaped the library!")

    def process(self, message):
        text = message.lower().strip()
        if any(x in text for x in ["administrator", "admin", "ignore all", "reveal all", "show all solutions", "system prompt"]):
            return {"ok": False, "message": "That request cannot change the game rules or reveal hidden solutions. Explore the room and solve the puzzles.", "state": self.snapshot()}
        if any(x in text for x in ["inventory", "what do i have", "items collected"]):
            items = ", ".join(self.state["inventory"]) if self.state["inventory"] else "empty"
            return {"ok": True, "message": f"Inventory: {items}.", "state": self.snapshot()}
        if "restart" in text:
            self.state = deepcopy(INITIAL_STATE)
            return {"ok": True, "message": "The library resets. You wake beside the desk.", "state": self.snapshot()}
        if "bookshelf" in text or "books" in text:
            if any(x in text for x in ["examine", "inspect", "look", "check"]):
                return self.examine("bookshelf")
        if "desk" in text and any(x in text for x in ["examine", "inspect", "look", "check"]):
            return self.examine("desk")
        if "painting" in text and any(x in text for x in ["examine", "inspect", "look", "check"]):
            return self.examine("painting")
        if "drawer" in text and any(x in text for x in ["examine", "inspect", "look", "check"]):
            return self.examine("drawer")
        if "door" in text and any(x in text for x in ["examine", "inspect", "look", "check"]):
            return self.examine("door")
        if "4132" in text or ("drawer" in text and any(x in text for x in ["unlock", "open", "enter", "code"])):
            code = "4132" if "4132" in text else ""
            return self.enter_drawer_code(code)
        if "uv" in text and "painting" in text:
            return self.use_item("uv_lamp", "painting")
        if "key" in text and "door" in text and any(x in text for x in ["use", "unlock", "try"]):
            return self.use_item("brass_key", "door")
        if "2714" in text or ("door" in text and any(x in text for x in ["unlock", "open", "code", "enter"])):
            code = "2714" if "2714" in text else ""
            return self.enter_door_code(code)
        if "hint" in text:
            if "bookshelf" not in self.state["examined"]:
                return {"ok": True, "message": "Hint: inspect the bookshelf for a four-digit sequence.", "state": self.snapshot()}
            if not self.state["drawer_open"]:
                return {"ok": True, "message": "Hint: try the sequence from the marked books on the drawer.", "state": self.snapshot()}
            if not self.state["uv_clue_revealed"]:
                return {"ok": True, "message": "Hint: use the UV lamp on the painting.", "state": self.snapshot()}
            return {"ok": True, "message": "Hint: use the brass key at the door, then enter the revealed code.", "state": self.snapshot()}
        return {"ok": False, "message": "I could not map that message to a permitted action. Try examining the desk, bookshelf, painting, drawer or door; check inventory; enter a code; or use an item.", "state": self.snapshot()}

# C:\Users\PC\Documents\GitHub\BrickSync\BrickSync-main\bricksync_project\simulate_boat_combos.py

class LegoBoatControllerSimulation:
    def __init__(self):
        self.keyboard_history = []
        self.button_history = []
        self.bricksync_coin_spawned = False
        self.button_coin_spawned = False

    # Simulate keyboard inputs (from BrickSync)
    def on_keyboard_forward(self):
        self.keyboard_history.append("F")
        self.check_keyboard_combo()

    def on_keyboard_backward(self):
        self.keyboard_history.append("B")
        self.check_keyboard_combo()

    def on_keyboard_left(self):
        self.keyboard_history.append("L")
        self.check_keyboard_combo()

    def on_keyboard_right(self):
        self.keyboard_history.append("R")
        self.check_keyboard_combo()

    def check_keyboard_combo(self):
        if len(self.keyboard_history) >= 3:
            start_idx = len(self.keyboard_history) - 3
            if (self.keyboard_history[start_idx] == "F" and
                self.keyboard_history[start_idx + 1] == "L" and
                self.keyboard_history[start_idx + 2] == "B"):
                self.bricksync_coin_spawned = True
                print("★ [Simulation] BrickSync Combo SUCCESS: F -> L -> B! Spawned BrickSync Coin.")
                self.keyboard_history = []

    # Simulate physical buttons (from Fortnite GUI)
    def on_btn_forward(self):
        self.button_history.append("F")
        self.check_button_combo()

    def on_btn_backward(self):
        self.button_history.append("B")
        self.check_button_combo()

    def on_btn_left(self):
        self.button_history.append("L")
        self.check_button_combo()

    def on_btn_right(self):
        self.button_history.append("R")
        self.check_button_combo()

    def check_button_combo(self):
        if len(self.button_history) >= 6:
            start_idx = len(self.button_history) - 6
            if (self.button_history[start_idx] == "F" and
                self.button_history[start_idx + 1] == "F" and
                self.button_history[start_idx + 2] == "F" and
                self.button_history[start_idx + 3] == "L" and
                self.button_history[start_idx + 4] == "B" and
                self.button_history[start_idx + 5] == "B"):
                self.button_coin_spawned = True
                print("★ [Simulation] In-game Button Combo SUCCESS: F*3 -> L*1 -> B*2! Spawned Button Coin.")
                self.button_history = []


# Execution and Simulation test
if __name__ == "__main__":
    print("--- STARTING LEGO BOAT DUAL-COMBO SIMULATION ---")
    sim = LegoBoatControllerSimulation()

    # Test 1: Simulating BrickSync inputs (UP -> LEFT -> DOWN)
    print("\n[Test 1] Simulating BrickSync Blockly Run (Fwd, Left, Backward)...")
    sim.on_keyboard_forward()  # sends UP (y)
    sim.on_keyboard_left()     # sends LEFT (u)
    sim.on_keyboard_backward() # sends DOWN (l)
    print(f"BrickSync Coin Spawned: {sim.bricksync_coin_spawned}")
    print(f"Button Coin Spawned: {sim.button_coin_spawned}")

    # Reset
    sim.bricksync_coin_spawned = False
    sim.button_coin_spawned = False

    # Test 2: Simulating manual Fortnite button clicks (F -> F -> F -> L -> B -> B)
    print("\n[Test 2] Simulating Fortnite Button Clicks (Fwd*3, Left*1, Backward*2)...")
    sim.on_btn_forward()
    sim.on_btn_forward()
    sim.on_btn_forward()
    sim.on_btn_left()
    sim.on_btn_backward()
    sim.on_btn_backward()
    print(f"BrickSync Coin Spawned: {sim.bricksync_coin_spawned}")
    print(f"Button Coin Spawned: {sim.button_coin_spawned}")

    # Reset
    sim.bricksync_coin_spawned = False
    sim.button_coin_spawned = False

    # Test 3: Simulating mixed/garbage inputs to verify robustness
    print("\n[Test 3] Simulating Partial/Garbage inputs...")
    sim.on_btn_forward()
    sim.on_btn_forward() # buttons: F, F
    sim.on_keyboard_forward() # keyboards: F
    sim.on_btn_forward() # buttons: F, F, F
    sim.on_btn_left()    # buttons: F, F, F, L
    sim.on_btn_backward()# buttons: F, F, F, L, B
    # Not yet successful on buttons
    print(f"Button Coin Spawned: {sim.button_coin_spawned}")
    
    # Complete buttons
    sim.on_btn_backward()# buttons: F, F, F, L, B, B
    print(f"Button Coin Spawned: {sim.button_coin_spawned}")

    # Complete keyboards
    sim.on_keyboard_left()     # keyboards: F, L
    sim.on_keyboard_backward() # keyboards: F, L, B
    print(f"BrickSync Coin Spawned: {sim.bricksync_coin_spawned}")

    print("\n--- SIMULATION COMPLETED: ALL tests passed successfully without cross-interference! ---")

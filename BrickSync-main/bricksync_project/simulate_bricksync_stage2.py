# BrickSync Stage 2 End-to-End Simulation
import time

# PC keyboard triggers mapped to Fortnite Verse variables
class FortniteSubmarine:
    def __init__(self):
        self.RightCount = 0
        self.LeftCount = 0
        self.IsCoinSpawned = False
        self.IsCoinCollected = False

    def on_press_h(self):
        # TriggerLeft_CCW (H)
        self.LeftCount += 1
        print(f" [Fortnite] 'H' Key Pressed (TriggerLeft_CCW) -> CCW: {self.LeftCount}/3, CW: {self.RightCount}/3")
        self.check_combo()

    def on_press_j(self):
        # TriggerRight_CW (J)
        self.RightCount += 1
        print(f" [Fortnite] 'J' Key Pressed (TriggerRight_CW) -> CCW: {self.LeftCount}/3, CW: {self.RightCount}/3")
        self.check_combo()

    def check_combo(self):
        if not self.IsCoinSpawned:
            if self.RightCount >= 3 and self.LeftCount >= 3:
                self.IsCoinSpawned = True
                print(" ★ [Fortnite] SUCCESS: Submarine combo met! BrickSyncSpawner.SpawnItem() called.")

    def collect_coin(self):
        if self.IsCoinSpawned:
            self.IsCoinCollected = True
            self.IsCoinSpawned = False
            self.RightCount = 0
            self.LeftCount = 0
            print(" ★ [Fortnite] Coin Collected! All counts reset to 0.")

# Python Bridge Server emulation
def run_bridge_server(submarine):
    # Simulated WebSocket commands from BrickSync SPA page
    commands = [
        ("wait", 5.0),
        ("motor_cw", 3),  # CW 3 times (sends 'h' to Fortnite)
        ("motor_ccw", 3), # CCW 3 times (sends 'j' to Fortnite)
    ]
    
    print("\n--- Starting Bridge Server Communication ---")
    for cmd, val in commands:
        if cmd == "wait":
            print(f" [Bridge] Waiting for {val} seconds...")
            time.sleep(0.1) # simulated delay
        elif cmd == "motor_cw":
            print(" [Bridge] CW Block running (3 units)")
            for i in range(val):
                print(" [Bridge] Sending 'h' keypress...")
                submarine.on_press_h()
                time.sleep(0.1) # simulated delay between pulses
        elif cmd == "motor_ccw":
            print(" [Bridge] CCW Block running (3 units)")
            for i in range(val):
                print(" [Bridge] Sending 'j' keypress...")
                submarine.on_press_j()
                time.sleep(0.1) # simulated delay between pulses

if __name__ == "__main__":
    sub = FortniteSubmarine()
    run_bridge_server(sub)
    sub.collect_coin()

# Submarine Non-Seated Global Trigger Simulation
import time

class FortniteSubmarineNonSeated:
    def __init__(self):
        self.RightCount = 0
        self.LeftCount = 0
        self.IsCoinSpawned = False
        self.IsMoving = False
        self.CurrentDriver = None # None means player is standing outside

    def on_press_h(self, player):
        # TriggerLeft_CCW triggers globally (no seated check)
        if not self.IsMoving:
            self.LeftCount += 1
            self.IsMoving = True
            print(f" [Submarine] CCW Rotated by Player {player} -> Left: {self.LeftCount}/3, Right: {self.RightCount}/3")
            self.check_combo(player)
            # Simulated movement time
            self.IsMoving = False

    def on_press_j(self, player):
        # TriggerRight_CW triggers globally (no seated check)
        if not self.IsMoving:
            self.RightCount += 1
            self.IsMoving = True
            print(f" [Submarine] CW Rotated by Player {player} -> Left: {self.LeftCount}/3, Right: {self.RightCount}/3")
            self.check_combo(player)
            # Simulated movement time
            self.IsMoving = False

    def check_combo(self, player):
        if not self.IsCoinSpawned:
            if self.RightCount >= 3 and self.LeftCount >= 3:
                self.IsCoinSpawned = True
                print(f" ★ [Submarine] SUCCESS: Combo met by Player {player}! Spawning Coin from BrickSyncSpawner.")

def run_simulation():
    sub = FortniteSubmarineNonSeated()
    print("\n--- Running Non-Seated Rotation Combo Simulation ---")
    
    # Simulate a player standing outside and executing the BrickSync code (Wait 5s -> CW 3 -> CCW 3)
    player = "Player1"
    
    # 1. CW 3 (triggers H key 3 times)
    for i in range(3):
        sub.on_press_h(player)
        
    # 2. CCW 3 (triggers J key 3 times)
    for i in range(3):
        sub.on_press_j(player)

if __name__ == "__main__":
    run_simulation()

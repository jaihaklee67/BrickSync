# Submarine Double-Combo Simulation
RightCount = 0
LeftCount = 0
BtnForwardCount = 0
BtnBackwardCount = 0
IsCoinSpawned = False

def check_combo():
    global IsCoinSpawned
    if IsCoinSpawned:
        return
        
    # Condition 1: BrickSync Rotation Combo (Right 3, Left 3)
    bs_success = (RightCount >= 3) and (LeftCount >= 3)
    
    # Condition 2: Fortnite Button Combo (Forward 3, Backward 2)
    btn_success = (BtnForwardCount >= 3) and (BtnBackwardCount >= 2)
    
    if bs_success:
        IsCoinSpawned = True
        print(f" -> [Spawning Coin] Reason: BrickSync combo met (Right: {RightCount}, Left: {LeftCount})")
    elif btn_success:
        IsCoinSpawned = True
        print(f" -> [Spawning Coin] Reason: Fortnite Button combo met (Forward: {BtnForwardCount}, Backward: {BtnBackwardCount})")

def pick_up_coin():
    global IsCoinSpawned, RightCount, LeftCount, BtnForwardCount, BtnBackwardCount
    if IsCoinSpawned:
        print(" -> [Coin Picked Up] Mission Completed successfully!")
        # Reset state
        IsCoinSpawned = False
        RightCount = 0
        LeftCount = 0
        BtnForwardCount = 0
        BtnBackwardCount = 0
    else:
        print(" -> Cannot pick up coin (No coin spawned)")

# Trigger simulation functions
def run_bricksync_combo():
    global RightCount, LeftCount
    print("\n--- Running Scenario A: BrickSync (Right 3, Left 3) ---")
    for i in range(3):
        RightCount += 1
        check_combo()
    for i in range(3):
        LeftCount += 1
        check_combo()
    pick_up_coin()

def run_btn_combo():
    global BtnForwardCount, BtnBackwardCount
    print("\n--- Running Scenario B: Fortnite Buttons (Forward 3, Backward 2) ---")
    for i in range(3):
        BtnForwardCount += 1
        check_combo()
    for i in range(2):
        BtnBackwardCount += 1
        check_combo()
    pick_up_coin()

if __name__ == "__main__":
    run_bricksync_combo()
    run_btn_combo()

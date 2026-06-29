# Submarine Double-Combo Simulation with Forward 3 / Backward 3
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
    
    # Condition 2: Fortnite Button Combo (Forward 3, Backward 3)
    btn_success = (BtnForwardCount >= 3) and (BtnBackwardCount >= 3)
    
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
def run_btn_combo_3_3():
    global BtnForwardCount, BtnBackwardCount
    print("\n--- Running Scenario B (Updated): Fortnite Buttons (Forward 3, Backward 3) ---")
    for i in range(3):
        BtnForwardCount += 1
        check_combo()
    for i in range(3):
        BtnBackwardCount += 1
        check_combo()
    pick_up_coin()

if __name__ == "__main__":
    run_btn_combo_3_3()

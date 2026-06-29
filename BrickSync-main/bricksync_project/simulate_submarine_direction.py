# Direction Mapping Simulation
class DirectionSimulation:
    def __init__(self):
        self.angle = 0.0

    def simulate_step(self, action_type, step_increment):
        # Corrected Mapping:
        # CW (Right) -> positive direction (+1.0)
        # CCW (Left) -> negative direction (-1.0)
        direction_factor = 1.0 if action_type == "CW" else -1.0
        
        # Accumulate rotation angle
        self.angle += step_increment * direction_factor
        return self.angle

if __name__ == "__main__":
    sim = DirectionSimulation()
    
    # 1. Simulate Right (CW) block - 3 steps
    print("[Simulation] Running CW (Right) 3 block:")
    for i in range(3):
        angle = sim.simulate_step("CW", 360.0)
        print(f"  Step {i+1}: Cumulative Angle = {angle:.1f} degrees (Clockwise)")
        
    # 2. Simulate Left (CCW) block - 3 steps
    print("\n[Simulation] Running CCW (Left) 3 block:")
    for i in range(3):
        angle = sim.simulate_step("CCW", 360.0)
        print(f"  Step {i+1}: Cumulative Angle = {angle:.1f} degrees (Counter-Clockwise)")

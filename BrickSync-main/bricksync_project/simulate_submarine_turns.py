# Smooth Rotation and Turn Validation Simulation
import time

class SmoothSubmarineSimulation:
    def __init__(self):
        self.roll = 0.0
        self.is_moving = False
        self.movement_id = 0
        self.right_count = 0
        self.left_count = 0

    def start_rotation(self, direction, duration_seconds):
        self.is_moving = True
        self.movement_id += 1
        current_id = self.movement_id
        
        # Determine direction factor
        dir_factor = 1.0 if direction == "CCW" else -1.0
        
        print(f"\n[Simulation] Start Rotation ({direction}) for {duration_seconds}s (Target: {duration_seconds * 360} degrees)")
        
        # Simulate the tick loop (every 0.1 seconds)
        ticks = int(duration_seconds / 0.1)
        total_rotated = 0.0
        
        for tick in range(ticks):
            if self.is_moving and self.movement_id == current_id:
                # Add 36 degrees every 0.1s
                step = 36.0 * dir_factor
                self.roll += step
                total_rotated += abs(step)
                # print(f"  Tick {tick+1}/{ticks}: Rotated {abs(step)} degrees. Current Roll: {self.roll:.1f}")
                time.sleep(0.01) # fast simulation sleep
            else:
                break
                
        print(f"[Simulation] Rotation Stopped. Total Rotated: {total_rotated:.1f} degrees ({total_rotated/360.0:.2f} turns)")
        self.is_moving = False

    def stop_rotation(self):
        print("[Simulation] Stop Command Received.")
        self.is_moving = False

if __name__ == "__main__":
    sim = SmoothSubmarineSimulation()
    # Simulate CW 3 block (3 seconds)
    sim.start_rotation("CW", 3.0)
    sim.stop_rotation()
    
    # Simulate CCW 3 block (3 seconds)
    sim.start_rotation("CCW", 3.0)
    sim.stop_rotation()

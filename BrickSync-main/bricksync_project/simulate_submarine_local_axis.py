# Local Axis Rotation Simulation
import time
import math

class LocalAxisSimulation:
    def __init__(self):
        # Simulated local axis state (roll)
        self.local_roll = 0.0
        self.is_moving = False
        self.movement_id = 0

    def start_local_rotation(self, direction, duration_seconds):
        self.is_moving = True
        self.movement_id += 1
        current_id = self.movement_id
        
        dir_factor = 1.0 if direction == "CCW" else -1.0
        print(f"\n[Local Axis Sim] Start Rotation ({direction}) for {duration_seconds}s")
        
        ticks = int(duration_seconds / 0.1)
        total_rotated = 0.0
        
        for tick in range(ticks):
            if self.is_moving and self.movement_id == current_id:
                # Local rotation step: 36 degrees every 0.1s
                step = 36.0 * dir_factor
                self.local_roll += step
                total_rotated += abs(step)
                time.sleep(0.01) # fast simulation sleep
            else:
                break
                
        print(f"[Local Axis Sim] Stopped. Total Local Rotation: {total_rotated:.1f} degrees ({total_rotated/360.0:.2f} turns)")
        self.is_moving = False

if __name__ == "__main__":
    sim = LocalAxisSimulation()
    # Simulate CW 3 block (3 seconds)
    sim.start_local_rotation("CW", 3.0)
    # Simulate CCW 3 block (3 seconds)
    sim.start_local_rotation("CCW", 3.0)

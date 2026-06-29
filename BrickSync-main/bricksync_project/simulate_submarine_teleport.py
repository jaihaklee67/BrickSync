# Frame-by-Frame TeleportTo Rotation Simulation
import time

class TeleportSubmarineSimulation:
    def __init__(self):
        self.angle = 0.0
        self.is_moving = False
        self.movement_id = 0

    def start_teleport_rotation(self, direction, duration_seconds):
        self.is_moving = True
        self.movement_id += 1
        current_id = self.movement_id
        
        dir_factor = 1.0 if direction == "CCW" else -1.0
        print(f"\n[Teleport Sim] Start Rotation ({direction}) for {duration_seconds}s (Target: {duration_seconds * 360} degrees)")
        
        # Simulate 30Hz frame updates (every 0.033 seconds)
        ticks = int(duration_seconds / 0.033)
        total_rotated = 0.0
        
        for tick in range(ticks):
            if self.is_moving and self.movement_id == current_id:
                # Add step based on 360 degrees per second (12 degrees per 0.033s tick)
                step = 360.0 * 0.033 * dir_factor
                self.angle += step
                total_rotated += abs(step)
                # Simulated frame delay
                time.sleep(0.001) # fast simulation sleep
            else:
                break
                
        print(f"[Teleport Sim] Stopped. Total Rotated: {total_rotated:.1f} degrees ({total_rotated/360.0:.2f} turns)")
        self.is_moving = False

if __name__ == "__main__":
    sim = TeleportSubmarineSimulation()
    # Simulate CW 3 block (3 seconds)
    sim.start_teleport_rotation("CW", 3.0)
    # Simulate CCW 3 block (3 seconds)
    sim.start_teleport_rotation("CCW", 3.0)

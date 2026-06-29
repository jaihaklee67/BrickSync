# Overshoot and Correction Simulation
import math

def simulate_rotation(capped=False, force_initial_align=False):
    initial_angle = 0.0
    current_angle = 0.0
    brick_sync_rotate_axis = "Z"
    
    # 30Hz frame simulation
    step = 360.0 * 0.033333
    ticks = 0
    angles_logged = []
    
    # Simulating the loop logic
    while True:
        if current_angle < 360.0:
            current_angle += step
            ticks += 1
            
            # Applying capping logic if enabled
            display_angle = min(current_angle, 360.0) if capped else current_angle
            angles_logged.append(display_angle)
        else:
            break
            
    final_angle = angles_logged[-1]
    
    if force_initial_align:
        final_angle = 360.0
        
    return ticks, final_angle, angles_logged

if __name__ == "__main__":
    print("[Simulation 1: Current Uncapped Loop]")
    ticks, final_angle, logs = simulate_rotation(capped=False, force_initial_align=False)
    print(f"Total Ticks executed: {ticks}")
    print(f"Final Angle reached: {final_angle:.5f} degrees (Overshoot: {final_angle - 360.0:.5f} degrees)")
    print(f"Last 3 frames: {[round(x, 3) for x in logs[-3:]]}")
    
    print("\n[Simulation 2: Proposed 2-Stage Capped Loop with Align]")
    ticks_opt, final_angle_opt, logs_opt = simulate_rotation(capped=True, force_initial_align=True)
    print(f"Total Ticks executed: {ticks_opt}")
    print(f"Final Angle reached: {final_angle_opt:.5f} degrees (Overshoot: {final_angle_opt - 360.0:.5f} degrees)")
    print(f"Last 3 frames: {[round(x, 3) for x in logs_opt[-3:]]}")

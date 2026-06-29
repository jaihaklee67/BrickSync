# Blockly BLE Compiler Queue Generation Simulation

class Block:
    def __init__(self, action_type, val=None):
        self.action_type = action_type
        self.val = val

def compile_ble_queue(blocks, unit="5", includes_red_case=False):
    ble_queue = []
    current_ble_delay = 0
    
    for block in blocks:
        action = block.action_type
        
        if action == 'start':
            # Start block does not add delay
            pass
        elif action == 'flow_wait':
            current_ble_delay += (block.val * 1000)
        elif action == 'matrix_clear':
            ble_queue.push({"action": "matrix_clear", "delay": current_ble_delay})
            current_ble_delay += 300
        else:
            # Emulated Switch-Case
            is_matched = False
            
            # Cases: matrix_image, matrix_pixel
            if action in ['matrix_image', 'matrix_pixel']:
                is_matched = True
            
            # Optional corrected case
            if includes_red_case and action == 'matrix_pixel_red':
                is_matched = True
                
            if is_matched:
                colors = [9] * 9 # Simulated Red pixels
                ble_queue.append({"action": "matrix", "colors": colors, "delay": current_ble_delay})
                
    if unit == '5':
        # Post-clear queue addition
        ble_queue.append({"action": "matrix_clear", "delay": current_ble_delay + 2000})
        
    return ble_queue

if __name__ == "__main__":
    # Simulated Workspace: Play -> Wait 2s -> Red Light
    workspace_blocks = [
        Block('start'),
        Block('flow_wait', 2),
        Block('matrix_pixel_red')
    ]
    
    print("[Simulation 1: Current Compiler (matrix_pixel_red is missing)]")
    queue_bug = compile_ble_queue(workspace_blocks, unit="5", includes_red_case=False)
    print(f"Generated BLE Queue length: {len(queue_bug)}")
    for i, cmd in enumerate(queue_bug):
        print(f"  Command {i+1}: {cmd['action']} (Delay: {cmd['delay']}ms)")
        
    print("\n[Simulation 2: Corrected Compiler (matrix_pixel_red is added)]")
    queue_fixed = compile_ble_queue(workspace_blocks, unit="5", includes_red_case=True)
    print(f"Generated BLE Queue length: {len(queue_fixed)}")
    for i, cmd in enumerate(queue_fixed):
        if 'colors' in cmd:
            print(f"  Command {i+1}: {cmd['action']} (Colors: {cmd['colors'][0]}, Delay: {cmd['delay']}ms)")
        else:
            print(f"  Command {i+1}: {cmd['action']} (Delay: {cmd['delay']}ms)")

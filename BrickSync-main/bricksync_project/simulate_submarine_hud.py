# HUD Rendering and Tracking Conflict Simulation

class MockTrackerDevice:
    def __init__(self, name):
        self.name = name
        self.value = 0
        
    def increment(self):
        self.value += 1
        
    def get_value(self):
        return self.value

class SubmarineControllerSim:
    def __init__(self, tracker):
        self.tracker = tracker
        self.canvas_map = {} # Isolated local canvas map

    def show_hud(self, player_id):
        # Adds Submarine HUD
        val = self.tracker.get_value()
        self.canvas_map[player_id] = f"[Submarine HUD: {val}/8]"
        print(f"  -> Added {self.canvas_map[player_id]}")

    def remove_hud(self, player_id):
        if player_id in self.canvas_map:
            print(f"  -> Removed {self.canvas_map[player_id]}")
            del self.canvas_map[player_id]

class FerrisWheelControllerSim:
    def __init__(self, tracker):
        self.tracker = tracker
        self.canvas_map = {} # Isolated local canvas map

    def show_hud(self, player_id):
        # Adds Ferris Wheel HUD
        val = self.tracker.get_value()
        self.canvas_map[player_id] = f"[Ferris Wheel HUD: {val}/8]"
        print(f"  -> Added {self.canvas_map[player_id]}")

    def remove_hud(self, player_id):
        if player_id in self.canvas_map:
            print(f"  -> Removed {self.canvas_map[player_id]}")
            del self.canvas_map[player_id]

# Simulated Global UI stack of the Player's Fortnite screen
class PlayerScreen:
    def __init__(self):
        self.active_widgets = []
        
    def add_widget(self, name):
        self.active_widgets.append(name)
        
    def remove_widget(self, name):
        if name in self.active_widgets:
            self.active_widgets.remove(name)

if __name__ == "__main__":
    print("[Simulation Case 1: Separate Trackers]")
    sub_tracker = MockTrackerDevice("SubmarineTracker")
    ferris_tracker = MockTrackerDevice("FerrisTracker")
    
    # 1. Earn coin on Submarine
    sub_tracker.increment()
    print(f"Submarine Tracker Value: {sub_tracker.get_value()}")
    
    # 2. Earn coin on Ferris Wheel
    ferris_tracker.increment()
    print(f"Ferris Wheel Tracker Value: {ferris_tracker.get_value()}")
    print("Conflict: Since trackers are separate, Ferris Wheel HUD reads its own tracker (value 1) instead of cumulative (value 2)!")

    print("\n[Simulation Case 2: UI Overlapping due to Isolated CanvasMaps]")
    screen = PlayerScreen()
    sub_controller = SubmarineControllerSim(sub_tracker)
    ferris_controller = FerrisWheelControllerSim(ferris_tracker)
    
    player = "Player1"
    
    # Player enters Submarine
    print("Player sits on Submarine:")
    sub_controller.show_hud(player)
    screen.add_widget(sub_controller.canvas_map[player])
    
    # Player exits Submarine (but Submarine controller fails to clear other widgets, only its own)
    print("Player exits Submarine:")
    sub_widget = sub_controller.canvas_map[player]
    sub_controller.remove_hud(player)
    screen.remove_widget(sub_widget)
    
    # Player enters Ferris Wheel
    print("Player sits on Ferris Wheel:")
    ferris_controller.show_hud(player)
    screen.add_widget(ferris_controller.canvas_map[player])
    
    # Submarine spawns coin and updates its HUD again, but cannot clean Ferris Wheel's HUD!
    print("Submarine spawns coin (Submarine controller adds HUD):")
    sub_controller.show_hud(player)
    screen.add_widget(sub_controller.canvas_map[player])
    
    print(f"Current Player Screen State: {screen.active_widgets}")
    print("Conflict: Both [Ferris Wheel HUD] and [Submarine HUD] are simultaneously active and overlapping on the screen!")

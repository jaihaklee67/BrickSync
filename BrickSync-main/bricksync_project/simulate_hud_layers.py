class PlayerScreen:
    def __init__(self):
        self.active_widgets = {} # maps controller name -> widget details

    def add_widget(self, name, widget_text):
        self.active_widgets[name] = widget_text
        print(f" [+] HUD Added by [{name}]: '{widget_text}'")
        self.show_screen()

    def remove_widget(self, name):
        if name in self.active_widgets:
            del self.active_widgets[name]
            print(f" [-] HUD Removed by [{name}]")
        self.show_screen()

    def show_screen(self):
        layers = list(self.active_widgets.values())
        print(f" [Screen State] Active Layers: {len(layers)} | Content: {layers}")
        if len(layers) > 1:
            print(" [WARNING] OVERLAP DETECTED! Multiple HUD layers drawing simultaneously!")
        else:
            print(" [OK] Screen looks clean and sharp.")

def simulate():
    screen = PlayerScreen()
    
    print("\n--- Game Starts (Initial State) ---")
    # No startup widgets added now
    screen.show_screen()
    
    print("\n--- Scenario 1: Player enters Ferris Wheel Mutator Zone ---")
    screen.add_widget("FerrisWheelController", "Ferris Wheel: 0 / 8")
    
    print("\n--- Scenario 2: Player exits Ferris Wheel Zone ---")
    screen.remove_widget("FerrisWheelController")
    
    print("\n--- Scenario 3: Player sits in Cave Car seat ---")
    screen.add_widget("CaveCarController", "Cave Car: 1 / 8")
    
    print("\n--- Scenario 4: Player exits Cave Car seat ---")
    screen.remove_widget("CaveCarController")
    
    print("\n--- Scenario 5: Player sits in Submarine seat ---")
    screen.add_widget("SubmarineController", "Submarine: 2 / 8")
    
    print("\n--- Scenario 6: Player exits Submarine seat ---")
    screen.remove_widget("SubmarineController")

if __name__ == "__main__":
    simulate()

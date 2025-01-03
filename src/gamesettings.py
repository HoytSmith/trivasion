import os
import json

class GameSettings():
    def __init__(self, dir, defaults_path, settings_path, options_path):
        #set filepaths to proper file locations
        os.makedirs(dir, exist_ok=True)
        self.defaults_path = os.path.join(dir, defaults_path)
        self.settings_path = os.path.join(dir, settings_path)
        self.options_path = os.path.join(dir, options_path)
        #prepare settings objects
        self.default_settings = {}
        self.game_settings = {}
        self.settings_options = {}
        self.selected_options = {}
        #start initial loading
        self.load_defaults()
        self.load_settings()
        self.load_all_options()
        self.load_selected_options()
    
    def load_defaults(self):
        if os.path.exists(self.defaults_path):
            with open(self.defaults_path, "r") as defaults_file:
                self.default_settings = json.load(defaults_file)
        else:
            raise FileNotFoundError(f"Could not find Default Settings File at {self.defaults_path}")
    
    def load_all_options(self):
        if os.path.exists(self.options_path):
            with open(self.options_path, "r") as options_file:
                self.settings_options = json.load(options_file)
        else:
            raise FileNotFoundError(f"Could not find Options Settings File at {self.options_path}")
    
    def load_selected_options(self):
        if len(self.game_settings) > 0:
            self.selected_options = self.game_settings.copy()
        elif len(self.default_settings) > 0:
            self.selected_options = self.default_settings.copy()

    def check_settings(self):
        missing_settings = 0
        for setting in self.default_settings:
            if setting not in self.game_settings:
                self.game_settings[setting] = self.default_settings[setting]
                missing_settings += 1
        return missing_settings

    def load_settings(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path, "r") as settings_file:
                self.game_settings = json.load(settings_file)
                if self.check_settings() > 0:
                    self.save_settings()
        else:
            self.check_settings()
            self.save_settings()
    
    def save_settings(self):
        with open(self.settings_path, "w") as settings_file:
            json.dump(self.game_settings, settings_file, indent=4)

    def get_setting(self, key):
        if key in self.game_settings:
            return self.game_settings[key]
        if key in self.default_settings:
            return self.default_settings[key]
        raise Exception(f"Could not find Game Setting: {key}")
    
    def get_selected_option(self, key):
        return self.selected_options[key]
    
    def get_selected_option_text(self, key):
        option = self.get_selected_option(key)
        if key == "fullscreen":
            if option == True:
                return "On"
            else:
                return "Off"
        if key == "resolution":
            return f"{option[0]}x{option[1]}"
        return str(option)

    def get_selected_option_index(self, key):
        options = self.settings_options[key]
        selected = self.selected_options[key]
        for i in range(len(options)):
            if options[i] == selected:
                return i
        return -1   # represents a failure
    
    def get_all_selected_indices(self):
        all_indices = {}
        for key in self.settings_options:
            all_indices[key] = self.get_selected_option_index(key)
        return all_indices

    def apply_selection_options(self):
        changed_flags = {}
        if len(self.selected_options) > 0:
            for option in self.selected_options:
                changed_flags[option] = (self.game_settings[option] != self.selected_options[option])
            self.game_settings = self.selected_options.copy()
        self.save_settings()
        return changed_flags
    
    def select_next_option(self, key):
        current_index = self.get_selected_option_index(key)
        options = self.settings_options[key]
        next_index = current_index+1
        if next_index < len(options):
            self.selected_options[key] = options[next_index]
        return self.get_selected_option_text(key)

    def select_previous_option(self, key):
        current_index = self.get_selected_option_index(key)
        next_index = current_index-1
        if next_index >= 0:
            self.selected_options[key] = self.settings_options[key][next_index]
        return self.get_selected_option_text(key)

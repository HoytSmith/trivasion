import os
import json

class GameSettings():
    def __init__(self, dir, defaults_path, settings_path):
        #set filepaths to proper file locations
        os.makedirs(dir, exist_ok=True)
        self.defaults_path = os.path.join(dir, defaults_path)
        self.settings_path = os.path.join(dir, settings_path)
        #prepare settings objects
        self.default_settings = {}
        self.game_settings = {}
        #start initial loading
        self.load_defaults()
        self.load_settings()
    
    def load_defaults(self):
        if os.path.exists(self.defaults_path):
            with open(self.defaults_path, "r") as defaults_file:
                self.default_settings = json.load(defaults_file)
        else:
            raise FileNotFoundError(f"Could not find Default Settings File at {self.defaults_path}")

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
                if(self.check_settings() > 0):
                    self.save_settings()
        else:
            raise FileNotFoundError(f"Could not find Game Settings File at {self.settings_path}")
    
    def save_settings(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path, "w") as settings_file:
                json.dump(self.game_settings, settings_file, indent=4)
        else:
            raise FileNotFoundError(f"Could not find Game Settings File at {self.settings_path}")

    def get_setting(self, key):
        if key in self.game_settings:
            return self.game_settings[key]
        if key in self.default_settings:
            return self.default_settings[key]
        raise Exception(f"Could not find Game Setting: {key}")

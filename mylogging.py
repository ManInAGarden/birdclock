from datetime import datetime

class Logger:
    
    def __init__(self, filename):
        self.filename = filename
        self.mode = "INF"
        
    def set_mode(self, mode):
        self.mode = mode
        
    def write_message(self, mode, message):
        with open(self.filename, "a") as f:
            f.write("{0:%d.%m.%Y %H:%M:%S} - {1} - {2}\n".format(datetime.now(), mode, message))
            
            
    def write_info(self, message):
        if self.mode == "INF" or self.mode == "DBG":
            self.write_message("INF", message)
        
    def write_error(self, message):
        self.write_message("ERR", message)
        
    def write_debug(self, message):
        if self.mode == "DBG":
            self.write_message("DBG", message)

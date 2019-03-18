import configparser
import time
import threading
import os

class MinecraftWorldBackup():

    def load_config(self):
        self.config.read(self.cfg_filename)
        self.backup_directory = self.config['SETTINGS']['BackupDirectory']
        self.backup_interval_hrs = self.config['SETTINGS']['IntervalHours']
        self.backup_retention_amount = self.config['SETTINGS']['RetentionCount']
        self.server_directory = self.config['SETTINGS']['ServerDirectory']
        self.world_name = self.config['SETTINGS']['WorldName']

    def backup_worlds(self):
        
        last_backup_filename = ""
        print("Reading files in directory: " + self.backup_directory)
        backup_files = []
        for subdir, dirs, files in os.walk(self.backup_directory):
            for file in files:
                filename = os.path.join(subdir, file)
                print("reading filename: " + filename)
                try:
                    file_time = time.strptime(filename, self.world_name + "-%Y-%m-%d %H:%M:%S.tar.gz")
                    backup_files.append(filename)
                except ValueError:
                    print("Can't parse filename: " + filename)


    def __init__(self):
        self.config = configparser.ConfigParser()
        self.backup_directory = "."
        self.backup_interval_hrs = 6
        self.backup_retention_amount = 8
        self.server_directory = ""
        self.world_name = ""
        self.cfg_filename = "config.cfg"

        self.load_config()
        self.backup_worlds()

    def run(self):
        while True:
            time.sleep(1)

mwb = MinecraftWorldBackup()
#mwb.run()


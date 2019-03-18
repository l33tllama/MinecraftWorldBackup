import configparser
import time
import threading
import os
import datetime
import subprocess
class MinecraftWorldBackup():

    def load_config(self):
        self.config.read(self.cfg_filename)
        self.backup_directory = self.config['SETTINGS']['BackupDirectory']
        self.backup_interval_hrs = self.config['SETTINGS']['IntervalHours']
        self.backup_retention_amount = self.config['SETTINGS']['RetentionCount']
        self.server_directory = self.config['SETTINGS']['ServerDirectory']
        self.world_name = self.config['SETTINGS']['WorldName']
        self.screen_name = self.config['SETTINGS']['ScreenSessionName']

    def do_backup(self, time):
        # Say backup starting.
        #screen -R Server1 -X stuff "say Backup starting. World no longer saving... $(printf '\r')"
        #subprocess.run(["screen", "-R" ,  self.screen_name , "-X", "stuff \"say Backup starting. World no longer saving. $(printf '\\r')\""])
        print("Calling system to say stuff")
        system_call = "screen -R " + self.screen_name + " -X stuff \"say Backup starting. World no longer saving. $(printf '\\r')\""
        os.system(system_call)
        print(system_call)

    def backup_worlds(self):
        
        # Look for existing backups in backup directory
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
        
        backup_time = 0

        # First time backup
        if len(backup_files) is 0:
            now = datetime.datetime.now()
            next_hour = now - datetime.timedelta(minutes=now.minute, seconds = now.second, microseconds = now.microsecond)
            next_hour = next_hour + datetime.timedelta(hours = 1)

            backup_time = (next_hour - now).total_seconds()
        else:
            pass

        #self.do_backup(backup_time)


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
        self.do_backup(datetime.datetime.now())

    def run(self):
        while True:
            time.sleep(1)

mwb = MinecraftWorldBackup()
#mwb.run()


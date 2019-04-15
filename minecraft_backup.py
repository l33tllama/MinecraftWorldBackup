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
        self.backup_retention_amount = int(self.config['SETTINGS']['RetentionCount'])
        self.server_directory = self.config['SETTINGS']['ServerDirectory']
        self.world_name = self.config['SETTINGS']['WorldName']
        self.screen_name = self.config['SETTINGS']['ScreenSessionName']

    def screen_mc_cmd(self, cmd):
        system_call = "screen -R " + self.screen_name + " -X stuff \"" + cmd + " $(printf '\\r')\""
        os.system(system_call)
        print(system_call)

    def do_backup(self, backup_time):
        # Say backup starting.
        #screen -R Server1 -X stuff "say Backup starting. World no longer saving... $(printf '\r')"
        #subprocess.run(["screen", "-R" ,  self.screen_name , "-X", "stuff \"say Backup starting. World no longer saving. $(printf '\\r')\""])
        print("Calling system to say stuff")
        self.screen_mc_cmd("say Backup starting. World no longer saving.")
        self.screen_mc_cmd("save-off")
        self.screen_mc_cmd("save-all")
        time.sleep(3)

        #tar -cpvzf /home/mc/Minecraft/Backups/Server1/minecraft-hour0.tar.gz /home/mc/Minecraft/Games/Server1 --exclude '/home/mc/Minecraft/Games/Server1/plugins/dynmap'

        backup_filename = os.path.join(self.backup_directory, self.world_name + "-" + datetime.datetime.strftime(backup_time, "%Y-%m-%d_%H:%M:%S") + ".tar.gz")
        server_world_dir = os.path.join(self.server_directory, self.world_name)
        backup_cmd = "tar -cpvzf " + backup_filename + " " + server_world_dir

        print("Backup cmd: " + backup_cmd)

        print("Running backup...")
        os.system(backup_cmd)
        print("Done.")

        self.screen_mc_cmd("save-on")
        self.screen_mc_cmd("say Backup complete. World now saving.")

        print("Running backup worlds again.")
        self.backup_worlds()

        #system_call = "screen -R " + self.screen_name + " -X stuff \"say Backup starting. World no longer saving. $(printf '\\r')\""
        #os.system(system_call)

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
                    file_time = time.strptime(file, self.world_name + "-%Y-%m-%d_%H:%M:%S.tar.gz")
                    backup_files.append(file)
                except ValueError:
                    print("Can't parse filename: " + filename)
        
        backup_time = 0

        next_hour = 0

        backup_files.sort()

        # First time backup
        if len(backup_files) is 0:
            now = datetime.datetime.now()
            next_hour = now - datetime.timedelta(minutes=now.minute, seconds = now.second, microseconds = now.microsecond)
            next_hour = next_hour + datetime.timedelta(hours = 1)

            #backup_time = (next_hour - now).total_seconds()
            print("No previous backups, running backup immediately.")
            self.do_backup(now)
        
        # Backups already exist - find last one
        else:

            print("Backup exists.. scheduling next backup.")
            last_file = backup_files[len(backup_files) -1]
            last_file_time = datetime.datetime.strptime(last_file, self.world_name + "-%Y-%m-%d_%H:%M:%S.tar.gz")
            
            next_hour = last_file_time - datetime.timedelta(minutes=last_file_time.minute, seconds = last_file_time.second, microseconds = last_file_time.microsecond)
            next_hour = next_hour + datetime.timedelta(hours = 1)

            now = datetime.datetime.now()

            backup_time = (next_hour - now).total_seconds()

            print("Next backup in " + str(backup_time) + " seconds.")

            # Delete backup after retention count
            if(len(backup_files) > self.backup_retention_amount):
                first_file = backup_files[0]
                print("Deleting first file: " + first_file)
                os.remove(first_file)

            threading.Timer(backup_time, self.do_backup, [next_hour])

        # Set a timer thread for the next backup


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
mwb.run()


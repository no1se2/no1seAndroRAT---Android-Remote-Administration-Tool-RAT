import subprocess
import shutil
import os
def main():

    def run_command(command):
        """Run a shell command and print its output."""
        print(f"Executing: {command}")
        try:
            proc = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print(proc.stdout)
            if proc.returncode != 0:
                print(f"Command failed with return code {proc.returncode}")
                return False
            return True
        except Exception as e:
            print(f"Error executing command: {e}")
            return False

    # Define paths
    sources_list = "/etc/apt/sources.list"
    backup_file = "sources.backup"

    # Step 1: Force purge uninstall zipalign
    if not run_command("apt-get purge zipalign --auto-remove -y"):
        print("Error purging zipalign. Exiting.")
        exit(1)

    # Step 2: Backup the sources.list file
    try:
        print(f"Backing up {sources_list} to {backup_file}")
        shutil.copy(sources_list, backup_file)
    except Exception as e:
        print(f"Failed to back up {sources_list}: {e}")
        exit(1)

    # Step 3: Clear the sources.list file
    try:
        print(f"Clearing {sources_list}")
        with open(sources_list, "w") as file:
            file.write("")
    except Exception as e:
        print(f"Failed to clear {sources_list}: {e}")
        exit(1)

    # Step 4: Add new repository
    new_repo = "deb http://ftp.de.debian.org/debian buster main"
    try:
        print(f"Adding '{new_repo}' to {sources_list}")
        with open(sources_list, "w") as file:
            file.write(new_repo + "\n")
    except Exception as e:
        print(f"Failed to write to {sources_list}: {e}")
        exit(1)

    # Step 5: Run apt update
    if not run_command("apt update"):
        print("Error updating apt. Reverting changes.")
        shutil.copy(backup_file, sources_list)
        exit(1)

    # Step 6: Install zipalign
    if not run_command("apt install zipalign -y"):
        print("Error installing zipalign. Reverting changes.")
        shutil.copy(backup_file, sources_list)
        exit(1)

    # Step 7: Revert sources.list from the backup
    try:
        print(f"Restoring {sources_list} from {backup_file}")
        shutil.copy(backup_file, sources_list)
    except Exception as e:
        print(f"Failed to restore {sources_list} from backup: {e}")
        exit(1)

    # Final update after restoring original sources.list
    if not run_command("apt update"):
        print("Warning: Final apt update failed.")

    print("Script execution completed successfully.")

if __name__ == "__main__":
    main()
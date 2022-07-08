import subprocess
import os.path
import os

# ------------------------------------------------------------------------------------------------ #
#                                         GLOBAL VARIABLES                                         #
# ------------------------------------------------------------------------------------------------ #
types = (".mp4", ".mov", ".wmv", ".avi") # the tuple of file types
directory_to_recurse = r"Z:\Udemy_And_Misc_Downloads"

# ------------------------------------------------------------------------------------------------ #
#                        HELPER FUNCTION - USE FFMPEG TO GET VIDEO DURATION                        #
# ------------------------------------------------------------------------------------------------ #
def get_video_duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

# ------------------------------------------------------------------------------------------------ #
#                            HELPER FUNCTION - RUN A POWERSHELL COMMAND                            #
# ------------------------------------------------------------------------------------------------ #
def run_powershell_command(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

# ------------------------------------------------------------------------------------------------ #
#                                        MAIN PROGRAM START                                        #
# ------------------------------------------------------------------------------------------------ #
for root, dirs, files in os.walk(directory_to_recurse):
    for file in files:
        print()
        if file.endswith(types): # The arg can be a tuple of suffixes to look for
            full_path_and_file = os.path.join(root, file)
            filename_only = os.path.splitext(file)[0]
            extension_only = os.path.splitext(file)[1]
            print(full_path_and_file,"\n", filename_only,"\n", extension_only,"\n")
            # Is the video already a converted one with "._" in file string
            if "._" in file:
                print("Found an already converted video file...")
                # Is the "root" video file already deleted?
                root_video_file = file.replace("._","")
                if not os.path.exists(os.path.join(root, root_video_file)):
                    print("'PARENT' video already deleted. Continuing...")
                    continue
                # Else, if the root video file still exists
                else:
                    print("'PARENT' video still exists. Checking durations...")
                    # Check if the current file's duration is close to the same as
                    # the root video file
                    curr_file_length = get_video_duration(os.path.join(root, file))
                    root_file_length = get_video_duration(os.path.join(root, root_video_file))
                    print(curr_file_length, root_file_length)
                    if root_file_length * 0.97 > curr_file_length:
                        print("Current converted video wasn't done converting. Starting over...")
                        # Delete the current file, and re-run_powershell_command conversion
                        os.remove(os.path.join(root, file))
                        result = run_powershell_command("ffmpeg -i '" + full_path_and_file + 
                                            "' -y -vcodec libx264 -acodec ac3 -threads 2 '" + 
                                            str(root) + "\\" + str(filename_only) + "._" + 
                                            str(extension_only) + "'")
                        print("result:", result)
                        if result.returncode >= 1:
                            print("ERROR!")
                            exit(result.returncode)
                        os.remove(os.path.join(root, root_video_file))
                        continue
                    # Else, it's safe to delete the root video file
                    else:
                        print("Current converted video is same duration as ROOT video. Deleting root...")
                        os.remove(os.path.join(root, root_video_file))
                        continue
            elif "._" not in file:     
                # Check if video has already been downsampled
                if os.path.exists(os.path.join(root, filename_only + "._" + extension_only)):
                    root_file_length = get_video_duration(os.path.join(root, file))
                    conv_file_length = get_video_duration(os.path.join(root, filename_only + "._" + extension_only))
                    if root_file_length * 0.97 > conv_file_length:
                        print("Current converted video wasn't done converting. Starting over...")
                        # Delete the current file, and re-run_powershell_command conversion
                        os.remove(os.path.join(root, filename_only + "._" + extension_only))
                        result = run_powershell_command("ffmpeg -i '" + full_path_and_file + 
                                            "' -y -vcodec libx264 -acodec ac3 -threads 2 '" + 
                                            str(root) + "\\" + str(filename_only) + "._" + 
                                            str(extension_only) + "'")
                        print("result:", result)
                        if result.returncode >= 1:
                            print("ERROR!")
                            exit(result.returncode)
                        os.remove(os.path.join(root, full_path_and_file))
                        continue
                    else:
                        print("Current converted video is same duration as ROOT video. Deleting root...")
                        os.remove(os.path.join(root, full_path_and_file))
                        continue
                # Else, if video has NOT been downsampled yet, do it
                else:
                    print("No conversion done for this file yet. Starting it now...")
                    # Delete the current file, and re-run_powershell_command conversion
                    result = run_powershell_command("ffmpeg -i '" + full_path_and_file + 
                                            "' -y -vcodec libx264 -acodec ac3 -threads 2 '" + 
                                            str(root) + "\\" + str(filename_only) + "._" + 
                                            str(extension_only) + "'")
                    print("result:", result)
                    if result.returncode >= 1:
                        print("ERROR!")
                        exit(result.returncode)
                    os.remove(os.path.join(root, full_path_and_file))
                    continue
print("Done!")
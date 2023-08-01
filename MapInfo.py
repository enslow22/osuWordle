import ossapi
import subprocess, os, shutil

'''
This class grabs all the relevant map info with the DATABASE. All info is saved in this object.
'''

class MapInfo:
    def __init__(self, map_id, times=None, debug=False):

        # Clear static folder
        videos_path = os.path.join(os.getcwd(), "static", "videos")
        if os.path.exists(videos_path) and not debug:
            shutil.rmtree(videos_path)
            os.mkdir(videos_path)

        api = ossapi.OssapiV2(19967, "jiSzJ2f5gXD0NwyThwUc4P8uNPQRVkRYNutQAlpK")
        self.bmsinfo = api.beatmapset(beatmap_id=map_id)
        self.beatmap = api.beatmap(map_id)
        # scores = api.beatmap_scores(map_id).scores
        # self.best_play = scores[0]
        # self.best_player = api.user(self.best_play.user_id)
        self.mapper = api.user(self.bmsinfo.user_id)

        fails = self.beatmap.failtimes.fail
        fails.sort()

        failtimes = [i for i in range(len(fails)) if fails[i] == 0]
        highest_failtime = fails.index(fails[-1])
        highest_failtime2 = fails.index(fails[-2])

        # Each replay will have its own file. Right now this array stores the start time of the replay
        # It will be overwritten with the filename

        # Ideally, we want the first hint to start at the end of the intro and end 20 seconds after]
        # idk how to do this, so my best guess is the last fail time, or the total length - the active map length.
        if times is None:
            self.mp4_file_names = [min(failtimes[-1] * self.beatmap.total_length / 100,
                                       self.beatmap.total_length - self.beatmap.hit_length),
                                   max(highest_failtime - 10, 0), highest_failtime2 - 10]
        # Room for overriding
        elif len(times) == 3:
            self.mp4_file_names = times
        else:
            raise Exception("Please enter either no times or 3 times")

        if not debug:
            for i, time in enumerate(self.mp4_file_names):
                self.mp4_file_names[i] = self.getmp4(i, time, music=time == self.mp4_file_names[-1])
        else:
            self.mp4_file_names = [self.bmsinfo.title.replace(" ", "_") + str(i) + ".mp4" for i in range(len(self.mp4_file_names))]

    # Generate replay and save to static
    # Update later to save to db
    def getmp4(self, filenumber, start, length=20, music=False):
        settings = "HideBG"
        if music:
            settings = "HideBG+unmute"

        # Helpful paths / filenames
        mp4title = self.bmsinfo.title.replace(" ", "_").replace(":", "") + str(filenumber)
        mp4_file_name = mp4title + ".mp4"

        # danser location
        danser_path = os.path.join(os.getcwd(), "danser")

        # mp4 location in static folder
        mp4_path = os.path.join(os.getcwd(), "static", "videos", mp4_file_name)

        # Generate mp4
        # First try with id
        clistring = 'danser-cli.exe -skip -id="%s" -settings="%s" -start="%d" -end="%d" -out="%s"' % (
            self.beatmap.id, settings, start, start + length, mp4title)
        subprocess.run(clistring, cwd=danser_path, shell=True, check=True)

        # If that didn't work, try with title instead. Not sure why some ids dont work
        if not os.path.exists(os.path.join(danser_path, "videos", mp4_file_name)):
            print("Maybe map not downloaded")
            clistring = 'danser-cli.exe -skip -t="%s" -settings="%s" -start="%d" -end="%d" -out="%s"' % (
                self.bmsinfo.title, settings, start, start + length, mp4title)
            subprocess.run(clistring, cwd=danser_path, shell=True, check=True)

        # Add to static folder
        shutil.move(os.path.join(danser_path, "videos", mp4_file_name), mp4_path)

        return mp4_file_name

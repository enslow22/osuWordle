from sqlalchemy import create_engine, Column, String, Integer, Date, Float, BLOB, select, exists
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import ossapi
import os
import subprocess
import cloudinary.uploader

api = ossapi.OssapiV2(19967, "jiSzJ2f5gXD0NwyThwUc4P8uNPQRVkRYNutQAlpK")
cloudinary.config(
    cloud_name="df26yoxez",
    api_key="978976488971281",
    api_secret="xLpmw1jpaRX4ut9VSK1Ey2MtbXQ"
)

class Base(DeclarativeBase):
    pass

class osuMap(Base):
    __tablename__ = 'osuMapInfo'
    map_id = Column(Integer, primary_key=True)
    map_url = Column(String)

    # Song Details
    title = Column(String)
    artist = Column(String)
    language = Column(String)
    genre = Column(String)
    bpm = Column(Integer)

    # Beatmap Info
    map_length = Column(Integer)
    star_rating = Column(Float)
    diff_name = Column(String)
    play_count = Column(Integer)
    background = Column(String)
    release_date = Column(String)

    # Mapper Info
    mapper_name = Column(String)
    mapper_previous_names = Column(String)
    mapper_country = Column(Integer)

    # Media
    cloudinary_link_1 = Column(String)
    cloudinary_link_2 = Column(String)
    cloudinary_link_3 = Column(String)

    def generate_Media(self, number, start, length=15, music=False):

        print("Generating video number %s for: %s" % (str(number), str(self.title)))

        # Pick render settings
        settings = "HideBG"
        if music:
            settings = "HideBG+unmute"

        # File paths
        cwd = os.getcwd()
        danser_path = os.path.join(cwd, "danser")
        temp_path = os.path.join(cwd, "danser", "videos", "temp.mp4")

        # Clear temp folder
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # Danser saves files to danser/videos
        clistring = 'danser-cli.exe -skip -id="%s" -settings="%s" -start="%d" -end="%d" -out="%s"' % (
            self.map_id, settings, start, start + length, "temp")
        subprocess.run(clistring, cwd=danser_path, shell=True, check=True, stdout = subprocess.DEVNULL)

        if not os.path.exists(temp_path):
            print("Maybe map not downloaded")
            clistring = 'danser-cli.exe -skip -t="%s" -settings="%s" -start="%d" -end="%d" -out="%s"' % (
                self.title, settings, start, start + length, "temp")
            subprocess.run(clistring, cwd=danser_path, shell=True, check=True, stdout = subprocess.DEVNULL)

        # See if map exists
        if os.path.exists(temp_path):
            self.upload_Media(number)
            return 1
        else:
            return 0

    # TODO: MAKE SURE MEDIA DOES NOT ALREADY EXIST IN CLOUD
    def upload_Media(self, number):

        # Check if folder id already exists.
        # If so, delete and re-upload

        print("Attempting to upload video %s for: %s" % (number, self.title))

        data = cloudinary.uploader.upload(os.path.join(os.getcwd(), "danser", "videos", "temp.mp4"),
                                          resource_type='video',
                                          folder=str(self.map_id),
                                          public_id=self.title.replace("&", "and")+" "+str(number))

        if number == 1:
            self.cloudinary_link_1 = data['playback_url']
        elif number == 2:
            self.cloudinary_link_2 = data['playback_url']
        elif number == 3:
            self.cloudinary_link_3 = data['playback_url']


    # TODO: IF RECORD IS ALREADY IN DATABASE, DO NOT INITIALIZE
    def __init__(self, map_id):

        print("Accessing osu! api for map: %s" % (str(map_id)))

        bmsinfo = api.beatmapset(beatmap_id=map_id)
        beatmap = api.beatmap(map_id)
        mapper = api.user(bmsinfo.user_id)

        # Identifiers
        self.map_id = map_id
        self.map_url = beatmap.url

        # Song Details
        self.title = bmsinfo.title
        self.artist = bmsinfo.artist
        self.language = bmsinfo.language['name']
        self.genre = bmsinfo.genre['name']
        self.bpm = bmsinfo.bpm

        # Beatmap Details
        self.map_length = beatmap.total_length
        self.star_rating = beatmap.difficulty_rating
        self.diff_name = beatmap.version
        self.play_count = bmsinfo.play_count
        self.background = bmsinfo.covers.card
        self.release_date = str(bmsinfo.submitted_date)

        # Mapper Info
        self.mapper_name = mapper.username
        self.mapper_previous_names = str(mapper.previous_usernames)
        self.mapper_country = mapper.country.name

        # Media
        self.generate_Media(1, 10)
        self.generate_Media(2, 40)
        self.generate_Media(3, 70, music=True)

# errors: 3912664,
def addMaps(maps):
    for map_id in maps:
        map_exists = session.query(exists().where(osuMap.map_id == map_id)).scalar()
        # Check to see if map is not in db
        if not map_exists:
            new_osu_map = osuMap(map_id)
            session.add(new_osu_map)
            session.commit()
        else:
            print("%s already exists in database. Skipping" % str(map_id))

if __name__ == '__main__':
    engine = create_engine("sqlite+pysqlite:///instance/db.sqlite3", future=True)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    addMaps([119803, 3912664])

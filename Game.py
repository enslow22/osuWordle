from time import strftime, gmtime
from ast import literal_eval

class Game:
    def __init__(self, GameInfo):
        self.question_number = 0
        self.correct = False
        self.solution = GameInfo.title

        self.hint0 = {
            "mp4_url_name": GameInfo.cloudinary_link_1,
            "bpm": GameInfo.bpm
        }
        self.hint1 = {
            "mp4_url_name": GameInfo.cloudinary_link_2,
            "star_rating": GameInfo.star_rating
        }
        self.hint2 = {
            #"player_avatar": MapInfo.best_player.avatar_url,
            #"player_name": MapInfo.best_player.username,
            #"accuracy": MapInfo.best_play.accuracy,
            #"pp": MapInfo.best_play.pp,
            #"score": MapInfo.best_play.score,
            #"mods": MapInfo.best_play.mods,
            "map_length": strftime("%M:%S", gmtime(GameInfo.map_length)),
            "language": GameInfo.language,
            "genre": GameInfo.genre
        }
        self.hint3 = {
            #"mapper_avatar": MapInfo.mapper.avatar_url,
            "mapper_name": GameInfo.mapper_name,
            "previous_names": literal_eval(GameInfo.mapper_previous_names),
            "mapper_country": GameInfo.mapper_country,
            "release_date": GameInfo.release_date,
            "difficulty_name": GameInfo.diff_name,
            "number_of_plays": GameInfo.play_count
        }
        self.hint4 = {
            "bg": GameInfo.background,
            "difficulty_name": GameInfo.diff_name
        }
        self.hint5 = {
            "mp4_url_name": GameInfo.cloudinary_link_3
        }
        self.hint6 = {

        }

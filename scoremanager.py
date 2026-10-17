from json import dump, load, JSONDecodeError

class ScoreManager:
    def __init__(self, filepath="./highscores.json"):
        self.filepath = filepath
        self.autosave = True
        self.high_scores = self.getHighScores()

    def getHighScores(self):
        try:
            with open(self.filepath, 'r', encoding='utf8') as f:
                return load(f)['scores']
        except FileNotFoundError:
            print(f"Unable to find requested highscore file ({self.filepath}), creating file {self.filepath}")
            self.high_scores = []
            self.saveHighScores()
            return self.high_scores
        except (JSONDecodeError, KeyError) as e:
            raise Exception("Unable to parse JSON score data") from e

    def addHighScore(self, name, score):
        self.high_scores.append({'name': name, 'score': score})
        if self.autosave:
            self.saveHighScores()

    def saveHighScores(self):
        with open(self.filepath, 'w', encoding='utf8') as f:
            dump({'scores': self.high_scores}, f, indent=2)
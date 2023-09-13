from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm.attributes import flag_modified


db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    game_data = db.Column(db.PickleType())
    save_data = db.Column(db.PickleType())
    profile_picture = db.Column(db.String(255))

    def set_game_data(self, data):
        # Save modified game data
        self.game_data = data
        flag_modified(self, "game_data")  # Mark the attribute as modified
        db.session.commit()  # Commit the changes to the database

    def get_game_data(self):
        # Retrieves game data from db
        return self.game_data

    def save_game_data(self):
        # Creates a save game
        self.save_data = self.game_data
        flag_modified(self, "save_data")
        db.session.commit()

    def load_game_data(self):
        # Load a save game
        self.game_data = self.save_data
        flag_modified(self, "game_data")
        db.session.commit()
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_characters = Table(
    "favorite_characters",
    db.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("character_id", ForeignKey("character.id"))
)

fav = Table(
    "favorite_locations",
    db.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("location_id", ForeignKey("location.id"))
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    fav_characters: Mapped[list["Character"]] = relationship(secondary="favorite_characters",back_populates="likes_character")
    fav_locations: Mapped[list["Location"]] = relationship(secondary="favorite_locations", back_populates="likes_locations")
    

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "favorite_characters": (character.serialize() for character in self.fav_characters),
            "favorite_locations": (location.serializze() for location in self.fav_locations)
        }  

class Character(db.Model):
        id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
        name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
        quote: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
        image: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
        users_fav: Mapped[list["User"]] = relationship(secondary="favorite_characters",back_populates="likes_character")
        
        def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "quote": self.quote,
                "image_url": self.image,
                "favorite_of_users": (user.username for user in self.users_fav)
            }

class Location(db.Model):
        id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
        name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
        description: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
        image: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
        users_fav: Mapped[list["User"]] = relationship(secondary="favorite_locations",back_populates="likes_location")
        
        def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "image_url": self.image,
                "favorite_of_users": (user.username for user in self.users_fav)
            }
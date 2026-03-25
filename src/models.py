from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relationship One - Many
    favorite_planets: Mapped[list["FavoritePlanets"]] = relationship(
        "FavoritePlanets",
        back_populates="user"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    terrain: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[int] = mapped_column(Integer(), nullable=True)
    climate: Mapped[str] = mapped_column(String(120), nullable=True)

    # Relationship One - Many
    favorites: Mapped[list["FavoritePlanets"]] = relationship(
        "FavoritePlanets",
        back_populates="planet"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(120), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(120), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(120), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class FavoritePlanets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    # ForeignKeys
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))

    # Relationship Many - One
    user: Mapped["User"] = relationship(
        "User",
        back_populates="favorite_planets"
    )
    planet: Mapped["Planet"] = relationship(
        "Planet",
        back_populates="favorites"
    )

    def serialize(self):
        return {
            "id": self.id,
        }

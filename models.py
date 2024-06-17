from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Podcast(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str
    xml_url: str
    html_url: Optional[str]
    lang: str
    author: str
    description: str
    image_url: str
    episodes: List["Episode"] = Relationship(back_populates="podcast")


class Episode(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str
    duration: int
    description: str
    audio_url: str
    podcast_id: Optional[int] = Field(default=None, foreign_key="podcast.id")
    podcast: Podcast = Relationship(back_populates="episodes")


class PodcastsList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    podcasts: List[Podcast] = Relationship(back_populates="user")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str
    email: str
    password: str
    api_key: str
    subscription_id: Optional[int] = Field(default=None, foreign_key="subscription.id")
    subscriptions: List["Subscription"] = Relationship(back_populates="user")
    podcasts_list_id: Optional[int] = Field(default=None, foreign_key="podcastslist.id")
    podcasts_list: PodcastsList = Relationship(back_populates="user")


class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    podcast_id: Optional[int] = Field(default=None, foreign_key="podcast.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="subscriptions")
    podcast: Podcast = Relationship(back_populates="subscriptions")

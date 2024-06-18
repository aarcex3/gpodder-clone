from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str
    email: str
    password: str
    api_key: Optional[str] = Field(default=None)
    subscriptions: List["Subscription"] = Relationship(back_populates="user")
    podcasts_lists: List["PodcastsList"] = Relationship(back_populates="user")
    devices: List["Device"] = Relationship(back_populates="user")


class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    podcast_id: Optional[int] = Field(default=None, foreign_key="podcast.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="subscriptions")
    podcast: Podcast = Relationship(back_populates="subscriptions")


class PodcastsList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    description: Optional[str]
    podcasts: List["PodcastListItems"] = Relationship(back_populates="podcasts_list")


class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    device_name: str
    device_identifier: str = Field(unique=True)
    created_at: Optional[str] = Field(default=None)
    user: User = Relationship(back_populates="devices")


class Podcast(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str
    xml_url: str = Field(unique=True)
    html_url: Optional[str]
    lang: str
    author: str
    description: str
    image_url: str
    episodes: List["Episode"] = Relationship(back_populates="podcast")
    subscriptions: List["Subscription"] = Relationship(back_populates="podcast")


class Episode(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str
    duration: int
    description: str
    audio_url: str = Field(unique=True)
    podcast_id: Optional[int] = Field(default=None, foreign_key="podcast.id")
    podcast: Podcast = Relationship(back_populates="episodes")


class PodcastListItems(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    list_id: Optional[int] = Field(default=None, foreign_key="podcastslist.id")
    podcast_id: Optional[int] = Field(default=None, foreign_key="podcast.id")
    added_at: Optional[str] = Field(default=None)
    podcasts_list: PodcastsList = Relationship(back_populates="podcasts")
    podcast: Podcast = Relationship()


class ListenHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    episode_id: Optional[int] = Field(default=None, foreign_key="episode.id")
    listened_at: Optional[str] = Field(default=None)
    progress: Optional[int]
    user: User = Relationship()
    episode: Episode = Relationship()


class OPMLImportExport(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    action: str
    timestamp: Optional[str] = Field(default=None)
    user: User = Relationship()

-- Users Table
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Devices Table
CREATE TABLE Devices (
    device_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    device_name VARCHAR(255) NOT NULL,
    device_identifier VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Podcasts Table
CREATE TABLE Podcasts (
    podcast_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    feed_url VARCHAR(255) UNIQUE NOT NULL,
    website_url VARCHAR(255),
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Episodes Table
CREATE TABLE Episodes (
    episode_id INTEGER PRIMARY KEY AUTOINCREMENT,
    podcast_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    audio_url VARCHAR(255) UNIQUE NOT NULL,
    pub_date TIMESTAMP,
    duration INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (podcast_id) REFERENCES Podcasts(podcast_id)
);

-- Subscriptions Table
CREATE TABLE Subscriptions (
    subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    podcast_id INTEGER NOT NULL,
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (podcast_id) REFERENCES Podcasts(podcast_id),
    UNIQUE(user_id, podcast_id) -- Ensures a user can't subscribe to the same podcast multiple times
);

-- Listen History Table
CREATE TABLE ListenHistory (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    episode_id INTEGER NOT NULL,
    listened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    progress INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (episode_id) REFERENCES Episodes(episode_id),
    UNIQUE(user_id, episode_id) -- Ensures a user can't have multiple entries for the same episode
);

-- Podcast Lists Table
CREATE TABLE PodcastLists (
    list_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Podcast List Items Table
CREATE TABLE PodcastListItems (
    list_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER NOT NULL,
    podcast_id INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (list_id) REFERENCES PodcastLists(list_id),
    FOREIGN KEY (podcast_id) REFERENCES Podcasts(podcast_id),
    UNIQUE(list_id, podcast_id) -- Ensures a podcast can't be added multiple times to the same list
);

-- OPML Import/Export Table (Optional)
CREATE TABLE OPMLImportExport (
    opml_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    action TEXT CHECK(action IN ('import', 'export')) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

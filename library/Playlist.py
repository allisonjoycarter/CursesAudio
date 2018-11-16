import os

class Playlist:
    def __init__(self, name):
        """
        Constructor for a new playlist!
        Holds a name and a list of song paths
        """
        self.name = name
        self.songs = []

    def addSong(self, song):
        """
        Adds a song to the list
        @return false if song is not valid
        """
        if os.path.exists(song):
            self.songs.append(song)
        else:
            return False

    def removeSong(self, song):
        """
        Removes a song from the playlist

        @return false if song is not in list
        """
        if song in self.songs:
            self.songs.remove(song)
        else:
            return False

    def getName(self):
        """
        getter for the name of the list
        """
        return self.name

    def getSongs(self):
        """
        getter for the songs in playlist
        """
        return self.songs

import os
from library.Playlist import Playlist
from audioexceptions.CLI_Audio_Exception import *

class Library:
    def __init__(self):
        """
        Constructor for the library
        Makes empty lists for songs and playlists 
        Creates a playlist because of the way front end is setup
        You cannot make a playlist until you have one
        
        This design flaw should be fixed at some point
        """
        path = os.path.dirname(os.getcwd())
        self.songList = []
        myPlaylist = Playlist("List1")
        self.playlists = [myPlaylist]

    def addToLibrary(self, song):
        """
        Adds a given song path to the library

        @param song the path of the song to add
        """
        if os.path.exists(song):
            self.songList.append(song)
        else:
            #throws an error if it can't find the file
            #is this correct?
            raise CLI_Audio_File_Exception("File does not exist")
            return False

    def removeFromLibrary(self, song):
        """
        removes a given path to a song from the library
        
        @param song the path of the song to remove
        @return false if the song cannot be found
        """
        if song in self.songList:
            self.songList.remove(song)
        else:
            return False

    def getSongs(self):
        """
        Getter for the list of songs 
        in the library
        """
        return self.songList

    def makePlaylist(self, playlistName):
        """
        Creates an empty playlist given a name

        @param name of the new playlist
        @return the playlist created
        """        
        newPlaylist = Playlist(playlistName)
        self.playlists.append(newPlaylist)
        return newPlaylist

    def removePlaylist(self, playlist):
        """
        removes a playlist from the library
        
        @return false if the playlist does not exist
        """
        if playlist in self.playlists:
            self.playlists.remove(playlist)
        else:
            return False

    def addToPlaylist(self, playlist, song):
        """
        adds a song given a path to a selected playlist

        @param playlist the playlist to add to
        @song the path of the song to add to the playlist
        """
        if os.path.exists(song):
            if playlist in self.playlists:
                playlist.addSong(song)
                return True
        else:
            return False

    def removeFromPlaylist(self, playlist, song):
        """
        Removes a song given a path from a selected playlist

        @param playlist the playlist to remove from
        @param song the path of the song to remove
        @return false if the song is not in the list
        """
        if song in playlist.getSongs():
            playlist.removeSong(song)
        else:
            return False

    def getPlaylists(self):
        """
        Getter for the list of playlists
        """
        return self.playlists

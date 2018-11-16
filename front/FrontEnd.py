import curses
import curses.textpad

import sys
from math import ceil
from audioexceptions.CLI_Audio_Exception import *
class FrontEnd:

    def __init__(self, player, library):
        self.player = player
        self.library = library
        self.player.play(sys.argv[1])
        curses.wrapper(self.menu)

    def menu(self, args):
        self.stdscr = curses.initscr()

        #throw an error if the screen is too small
        if not all(i >= 30 for i in self.stdscr.getmaxyx()):
            raise CLI_Audio_Screen_Size_Exception("The screen is too small!")
        self.stdscr.border()
        self.stdscr.addstr(0,0, "cli-audio",curses.A_REVERSE)
        self.stdscr.addstr(5,10, "c - Change current song")
        self.stdscr.addstr(6,10, "p - Play/Pause")
        self.stdscr.addstr(7,10, "l - Library")
        self.stdscr.addstr(8,10, "o - playlist options")
        self.stdscr.addstr(9,10, "ESC - Quit")
        self.updateSong()
        self.stdscr.refresh()
        while True:
            c = self.stdscr.getch()
            if c == 27:
                self.quit()
            elif c == ord('p'):
                self.player.pause()
            elif c == ord('c'):
                self.changeSong()
                self.updateSong()
                self.stdscr.touchwin()
                self.stdscr.refresh()
            elif c == ord('l'):
                self.showLibrary()
                self.stdscr.touchwin()
                self.stdscr.refresh()
            #added another option, for dealing with playlists
            elif c == ord('o'):
                currentPlaylist = None

                """
                Makes a window to select a playlist, 
                then you can manipulate it with a different window
                """
                playlistWin = curses.newwin(10, 60, 10, 60)
                playlistWin.border()
                playlistWin.addstr(0,0, "Press the number playlist you want, or exit with ESC", curses.A_REVERSE)
                self.stdscr.refresh()
                curses.curs_set(False)
                curses.echo()
                # either print songs or tell user there isn't any
                if not self.library.getPlaylists():
                    playlistWin.addstr(1,1, "There are no playlists!", curses.A_REVERSE)
                else:
                    for x in range(len(self.library.getPlaylists())):
                        playlistWin.addstr(x + 1, 1, str(x) + " - " + self.library.getPlaylists()[x].getName(), curses.A_REVERSE)
                #get char that will be used as the index in list of playlists
                #start at 48 because that's 0 in ASCII
                playCom = 48
                while playCom != 27:
                    playCom = playlistWin.getch()
                    #for future reference, this can be changed to a string to allow for more than 10 playlists
                    if playCom - 48  < len(self.library.getPlaylists()) and playCom >= 48 and playCom <= 57:
                        currentPlaylist = self.library.getPlaylists()[playCom-48]
                        break
                curses.noecho()
                del playlistWin
                self.stdscr.touchwin()
                self.stdscr.refresh()
                curses.echo()

                #options window for manipulating lists
                optionsWin = curses.newwin(50,50,10,60)
                optionsWin.border()
                if currentPlaylist:
                    optionsWin.addstr(1,1, "No playlist is selected! Press esc to return.", curses.A_REVERSE)
                    command = 0
                    while command != 27:
                        command = optionsWin.getch()
                else:
                    #options to alter playlists
                    optionsWin.addstr(0,0, currentPlaylist.getName(), curses.A_REVERSE)
                    optionsWin.addstr(2,0, "n - new playlist", curses.A_REVERSE)
                    optionsWin.addstr(3,0, "a - add to playlist", curses.A_REVERSE)
                    optionsWin.addstr(4,0, "r - remove from playlist", curses.A_REVERSE)
                    optionsWin.addstr(5,0, "esc - leave menu", curses.A_REVERSE)

                    #print out songs in list
                    pos = 8
                    for i in range(len(currentPlaylist.getSongs())):
                        optionsWin.addstr(pos, 1, currentPlaylist.getSongs()[i],curses.A_REVERSE)
                        pos += 1
                    command = 0
                    while command != 27:
                        command = optionsWin.getch()
                        if command == ord('n'):
                            #create a playlist and set that to the selected one
                            currentPlaylist = self.createPlaylistWindow()
                            optionsWin.erase()
                            optionsWin.addstr(0,0, currentPlaylist.getName(), curses.A_REVERSE)
                            optionsWin.addstr(2,0, "n - new playlist", curses.A_REVERSE)
                            optionsWin.addstr(3,0, "a - add to playlist", curses.A_REVERSE)
                            optionsWin.addstr(4,0, "r - remove from playlist", curses.A_REVERSE)
                            optionsWin.addstr(5,0, "esc - leave menu", curses.A_REVERSE)
                        elif command == ord('a'):
                            self.addToPlaylistWindow(currentPlaylist)
                        elif command == ord('r'):
                            self.removeFromPlaylistWindow(currentPlaylist)
                        else:
                            pass
                curses.noecho()
                del optionsWin
                self.stdscr.touchwin()
                self.stdscr.refresh()
    
    def updateSong(self):
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    def changeSong(self):
        changeWindow = curses.newwin(5, 40, 5, 50)
        changeWindow.border()
        changeWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        self.player.stop()
        self.player.play(path.decode(encoding="utf-8"))
        
    def showLibrary(self):
        """this method creates a window used to select songs
        the code to make a scrollable menu has been adapted from:
        https://stackoverflow.com/questions/30795161/scroll-page-by-page-or-line-by-line-using-python-curses"""
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        libWindow = curses.newwin(30, 80, 5, 40)
        libWindow.border()
        
        #this was a big factor in making arrow keys work
        libWindow.keypad(1)

        libWindow.scrollok(1)
        libWindow.addstr(0,0, "Library: a = add song, r = remove selected song", curses.A_REVERSE)

        curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
        highlightText = curses.color_pair( 1 )
        normalText = curses.A_NORMAL
        songs = self.library.getSongs()
        max_row = 15
        row_num = len(songs)
        pages = int ( ceil(row_num/max_row))
        position = 1
        page = 1
        for i in range(1, max_row + 1):
            if row_num == 0:
                libWindow. addstr(1, 1, "There aren't any songs", highlightText)
            else:
                if (i == position):
                    libWindow.addstr(i, 2, str(i) + " - " + songs[i-1], highlightText)
                else:
                    libWindow.addstr(i, 2, str(i) + " - " + songs[i - 1], normalText)
                if i == row_num:
                    break
        self.stdscr.refresh()
        curses.echo()
        #commands to manipulate library
        c = 0
        while c != 27:
            c = libWindow.getch()
            if c == ord('a'):#add song
                self.addToLibrary()
                songs = self.library.getSongs()
                row_num = len(songs)
            elif c == ord('r'):#remove song
                if self.player.getCurrentSong() == songs[position - 1]:
                    self.player.stop()
                self.library.removeFromLibrary(songs[position - 1])
                songs = self.library.getSongs()
                row_num = len(songs)
                pages = int(ceil(row_num/max_row))
            elif c == ord('\n') and row_num != 0:#select song
                #this ends up showing a lot of errors for me about pyaudio
                self.player.stop()
                self.player.play(songs[position - 1])
                self.updateSong()
            elif c == curses.KEY_DOWN:
                if page == 1:
                    if position < i:
                        position = position + 1
                    else:
                        if pages > 1:
                            page = page + 1
                            position = 1 + (max_row * (page - 1))
                elif page == pages:
                    if position < row_num:
                        position = position + 1
                else:
                    if position < max_row + (max_row * (page - 1)):
                        position = position + 1
                    else:
                        page = page + 1
                        position = 1 + (max_row * (page - 1))
            elif c == curses.KEY_UP:
                if page == 1:
                    if position > 1:
                        position = position - 1
                else:
                    if position > ( 1 + ( max_row * ( page - 1 ) ) ):
                        position = position - 1
                    else:
                        page = page - 1
                        position = max_row + ( max_row * ( page - 1 ) )
            elif c == curses.KEY_LEFT:
                if page > 1:
                    page = page - 1
                    position = 1 + ( max_row * ( page - 1 ) )

            elif c == curses.KEY_RIGHT:
                if page < pages:
                    page = page + 1
                    position = ( 1 + ( max_row * ( page - 1 ) ) )
            
            libWindow.clrtoeol()
            libWindow.border()

            for i in range( 1 + ( max_row * ( page - 1 ) ), max_row + 1 + ( max_row * ( page - 1 ) ) ):
                if row_num == 0:
                    libWindow.addstr( 1, 1, "No songs in library",  highlightText )
                else:
                    if ( i + ( max_row * ( page - 1 ) ) == position + ( max_row * ( page - 1 ) ) ):
                        libWindow.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + songs[ i - 1 ], highlightText )
                    else:
                        libWindow.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + songs[ i - 1 ], normalText )
                    if i == row_num:
                        break
            self.stdscr.refresh()
            libWindow.refresh()

        del libWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()

    def addToLibrary(self):
        """
        Creates a window, gets input from user, and deletes a window
        to add a song to the library, shows a message if the file can't be found
        """
        addWindow = curses.newwin(5, 40, 10, 60)
        addWindow.border()
        addWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = addWindow.getstr(1,1, 30)
        curses.noecho()
        try:
            self.library.addToLibrary(path):
        except:
            addWindow.addstr(2, 1, "Unable to find file! Press esc to return to library.", curses.A_REVERSE)
            flag = addWindow.getch()
            #go until esc
            while flag != 27:
                flag = addWindow.getch()
        curses.noecho()
        del addWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()

    def createPlaylistWindow(self):
        """
        Creates a window for making a playlist
        and returns that playlist
        """
        createWin = curses.newwin(5, 40, 10, 60)
        createWin.border()
        createWin.addstr(0,0, "What is the name of new playlist?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        name = createWin.getstr(1,1,30)
        curses.noecho()
        newList = self.library.makePlaylist(name)
        curses.noecho()
        del createWin
        self.stdscr.touchwin()
        self.stdscr.refresh()
        return newList
    
    def addToPlaylistWindow(self, playlist):
        """
        creates a window to prompt a user for a song file 
        to add to a playlist

        @param playlist to add to
        """
        addWindow = curses.newwin(5, 40, 5, 30)
        addWindow.border()
        addWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = addWindow.getstr(1,1, 30)
        curses.noecho()
        if not self.library.addToPlaylist(playlist, path):
            addWindow.addstr(2, 1, "Unable to find file! Press esc to return to playlist.", curses.A_REVERSE)
            flag = addWindow.getch()
            while flag != 27:
                flag = addWindow.getch()
        curses.noecho()
        del addWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
    
    def removeFromPlaylistWindow(self, playlist):
        """
        Creates a window to remove a song from the current playlist
        per the user's input

        @param playlist to remove the song from
        """
        remWin = curses.newwin(5,40, 5, 30)
        remWin.border()
        remWin.addstr(0,0, "What song would you like to remove?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = remWin.getstr(1,1,30)
        curses.noecho()
        if not self.library.removeFromPlaylist(playlist,path):
            remWin.addstr(2, 1, "Unable to find song! Press esc to return to playlist.", curses.A_REVERSE)
        flag = remWin.getch()
        while flag != 27:
            flag = remWin.getch()
        curses.noecho()
        del remWin
        self.stdscr.touchwin()
        self.stdscr.refresh()


    def quit(self):
        self.player.stop()
        exit()


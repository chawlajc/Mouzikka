# import player
from cx_Oracle import *
from tkinter import messagebox
class model:
    def __init__(self):
        self.song_dict = {}
        self.song_dict_myfav = {}
        self.db_status = True
        self.conn = None
        self.cur = None
        try:
            self.conn = connect("mouzikka/music@127.0.0.1/xe")
            #print("Connected Successfully to the DB")
            self.cur = self.conn.cursor()
        except DatabaseError as ex:
            self.db_status = False
            print(ex)

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            #print("Cursor closed successfully")
        if self.conn is not None:
            self.conn.close()
            #print("Disconnected successfully from the DB")

    def add_song(self, song_name, song_path):
        self.song_dict[song_name] = song_path
        #print("Song added :", self.song_dict[song_name])

    def get_song_path(self, song_name):
        return self.song_dict[song_name]

    def remove_song(self, song_name):
        self.song_dict.pop(song_name)
        #print(self.song_dict)

    def search_song_in_favourites(self, song_name):
        self.cur.execute("Select song_name from Myfavourites where song_name=:1", (song_name,))
        x = self.cur.fetchone()
        if x is None:
            return False
        return True

    def add_song_to_favourites(self, song_name, song_path):
        x = self.search_song_in_favourites(song_name)
        if x:
            return ("Song already present in your favourites")
        else:
            self.cur.execute("select max(song_id) from Myfavourites")
            y = self.cur.fetchone()
            if y[0] is not None:
                song_id = y[0]+1
            else:
                song_id = 1
            self.cur.execute("Insert into Myfavourites values(:1, :2, :3)", (song_id, song_name, song_path))
            self.conn.commit()
            self.song_dict_myfav[song_name] = song_path
            return ("Song added to your favourites")

    def load_songs_from_favourites(self):
        self.cur.execute("Select song_name,song_path from Myfavourites")
        y = self.cur.fetchone()
        if y[0] is None:
            return ("No songs present in your Favourites")
        for song_name, song_path in self.cur:
            self.song_dict_myfav[song_name] = song_path
        self.song_dict = self.song_dict_myfav.copy()
        return ("List populated from favourites")

    def remove_song_from_favourites(self, song_name):
        self.cur.execute("Delete from Myfavourites where song_name=:1", (song_name,))
        n = 0
        n = self.cur.rowcount
        if n != 0:
            self.song_dict_myfav.pop(song_name)
            return ("Song deleted from your favourites")
        else:
            return ("Song not present in your favourites")



'''if __name__ == "__main__":
    p = player.player()
    print("DB Conn :", p.get_db_status())
    p.add_song()
'''


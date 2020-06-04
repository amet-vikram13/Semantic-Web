from graph_init import create_graph
from redis_proxy import get_connection
from redisgraph import Graph, Node, Edge
from redis.exceptions import ResponseError


class CreateTrackNode:
    def __init__(self, meta_dict):
        self.graph = create_graph()
        self.track = meta_dict['track']
        self.length = meta_dict['length']
        self.uri = meta_dict['uri']

    def current_song_present(self):
        query = 'MATCH (t:track) WHERE (t.uri="%s") RETURN t' % (self.uri)
        try:
            result = self.graph.query(query)
            result.result_set[1]
        except IndexError:
            return False
        except ResponseError:
            return False
        else:
            return True

    def create_track_node(self):
        if self.current_song_present():
            return False
        else:
            track_node = Node(label='track', properties={'name': self.track, 'length': self.length, 'uri': self.uri})
            self.graph.add_node(track_node)
            self.graph.commit()
            return True



class CreateArtistNode:
    def __init__(self, meta_dict):
        self.graph = create_graph()
        self.artist = meta_dict['artist']

    def current_artist_present(self):
        query = 'MATCH (a:artist) WHERE (a.name="%s") RETURN a' % (self.artist)
        try:
            result = self.graph.query(query)
            result.result_set[1]
        except IndexError:
            return False
        except ResponseError:
            return False
        else:
            return True


    def create_artist_node(self):
        if self.current_artist_present():
            return False
        else:
            artist_node = Node(label='artist', properties={'name': self.artist})
            self.graph.add_node(artist_node)
            self.graph.commit()
            return True



class CreateAlbumNode:
    def __init__(self, meta_dict):
        self.graph = create_graph()
        self.album = meta_dict['album']
        self.art_url = meta_dict['art_url']


    def current_album_present(self):
        query = 'MATCH (a:album) WHERE (a.name="%s") RETURN a' %(self.album)
        try:
            result = self.graph.query(query)
            result.result_set[1]
        except IndexError:
            return False
        except ResponseError:
            return False
        else:
            return True


    def create_album_node(self):
        if self.current_album_present():
            return False
        else:
            album_node = Node(label='album', properties={'name': self.album, 'art_url': self.art_url})
            self.graph.add_node(album_node)
            self.graph.commit()
            return True

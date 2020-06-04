import redis
from redis_proxy import get_connection
from graph_init import create_graph

class createTrackEdge:
    def __init__(self, meta_dict):
        self.graph = create_graph()
        self.redis_connection = get_connection()
        self.track = meta_dict['track']
        self.artist = meta_dict['artist']
        self.album = meta_dict['album']
        self.uri = meta_dict['uri']

    def create_artist_edge(self):
        query = 'MATCH (t:track), (a:artist) WHERE t.uri="%s" AND a.name="%s" CREATE (t)-[:performedby]->(a)' % (self.uri, self.artist)
        self.redis_connection.execute_command(
            'GRAPH.QUERY',
            'spotify',
            query
        )

    def create_album_edge(self):
        query = 'MATCH (t:track), (a:album) WHERE t.uri="%s" AND a.name="%s" CREATE (t)-[:belongsto]->(a)' %(self.uri, self.album)
        self.redis_connection.execute_command(
            'GRAPH.QUERY',
            'spotify',
            query
        )


class createArtistEdge:
    def __init__(self, meta_dict):
        self.graph = create_graph()
        self.redis_connection = get_connection()
        self.uri = meta_dict['uri']
        self.artist = meta_dict['artist']
        self.album = meta_dict['album']

    def create_track_edge(self):
        query = 'MATCH (a:artist), (t:track) WHERE a.name="%s" AND t.uri="%s" CREATE (a)-[:hastrack]->(t)' %(self.artist, self.uri)
        self.redis_connection.execute_command(
            'GRAPH.QUERY',
            'spotify',
            query
        )

    def create_album_edge(self):
        query = 'MATCH (a:artist), (b:album) WHERE a.name="%s" AND b.name="%s" CREATE (a)-[:hasalbum]->(b)' %(self.artist, self.album)
        self.redis_connection.execute_command(
            'GRAPH.QUERY',
            'spotify',
            query
        )


class createAlbumEdge:
    def __init__(self, meta_dict):
        self.graph = create_graph()
        self.redis_connection = get_connection()
        self.uri = meta_dict['uri']
        self.artist = meta_dict['artist']
        self.album = meta_dict['album']

    def create_track_edge(self):
        query = 'MATCH (a:album), (t:track) WHERE a.name="%s" AND t.uri="%s" CREATE (a)-[:containstrack]->(t)' %(self.album, self.uri)
        self.redis_connection.execute_command(
            'GRAPH.QUERY',
            'spotify',
            query
        )

    def create_artist_edge(self):
        query = 'MATCH (a:album), (ar:artist) WHERE a.name="%s" AND ar.name="%s" CREATE (a)-[:albumby]->(ar)' %(self.album, self.artist)
        self.redis_connection.execute_command(
            'GRAPH.QUERY',
            'spotify',
            query
        )

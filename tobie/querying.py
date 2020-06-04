from graphviz import Digraph
from importlib import reload
from redis_proxy import get_connection
from graph_init import create_graph
from spotify_interface import process_metadata, display_art
from create_nodes import CreateTrackNode, CreateArtistNode, CreateAlbumNode
from create_edges import createAlbumEdge, createTrackEdge, createArtistEdge


spotify_graph = Digraph(comment='Visualization of the redis graph', format='svg')
spotify_graph.graph_attr['rankdir'] = 'LR'


def add_nodes_digraph():
    meta_dict = process_metadata.get_meta_dict()
    spotify_graph.node(meta_dict['track'], meta_dict['track'])
    spotify_graph.node(meta_dict['album'], meta_dict['album'])
    spotify_graph.node(meta_dict['artist'], meta_dict['artist'])


def add_edges_digraph():
    meta_dict = process_metadata.get_meta_dict()
    spotify_graph.edge(meta_dict['track'], meta_dict['album'], 'track->album')
    spotify_graph.edge(meta_dict['album'], meta_dict['track'], 'album->track')
    spotify_graph.edge(meta_dict['track'], meta_dict['artist'], 'track-artist')
    spotify_graph.edge(meta_dict['artist'], meta_dict['track'], 'artist-track')
    spotify_graph.edge(meta_dict['album'], meta_dict['artist'], 'album-artist')
    spotify_graph.edge(meta_dict['artist'], meta_dict['album'], 'artist-album')


def process_result_set(result):
    for subset in result.result_set:
        for item in range(len(subset)):
            subset[item] = subset[item].decode('utf-8')


class queryFacade:
    def __init__(self):
        self.graph = create_graph()
        self.redis_connection = get_connection()

    def get_songs(self):
        query = 'MATCH (track:track) RETURN track.name, track.length, track.uri'
        result = self.graph.query(query)
        process_result_set(result)
        result.pretty_print()

    def get_artists(self):
        query = 'MATCH (artist:artist) RETURN artist.name'
        result = self.graph.query(query)
        process_result_set(result)
        result.pretty_print()

    def get_albums(self):
        query = 'MATCH (album:album) RETURN album.name, album.art_url'
        result = self.graph.query(query)
        process_result_set(result)
        result.pretty_print()

    def get_tracks_by_artist(self, artist_name):
        query = 'MATCH (track:track)-[:performedby]->(:artist {name:"%s"}) RETURN track.name' %(artist_name)
        result = self.graph.query(query)
        process_result_set(result)
        result.pretty_print()

    def get_tracks_by_album(self, album_name):
        query = 'MATCH (track:track)-[:belongsto]->(:album {name:"%s"}) RETURN track.name, track.length, track.uri' %(album_name)
        result = self.graph.query(query)
        process_result_set(result)
        result.pretty_print()

    def get_albums_by_artist(self, artist_name):
        query = 'MATCH (album:album)-[:albumby]->(:artist {name: "%s"}) RETURN album.name' %(artist_name)
        result = self.graph.query(query)
        process_result_set(result)
        result.pretty_print()

    def get_artist_by_album(self, album_name):
        query = 'MATCH (artist:artist)-[:hasalbum]->(:album {name:"%s"}) RETURN artist.name' %(album_name)
        result = self.graph.query(query)
        process_result_set(result)
        result.pretty_print()

    def get_album_by_track(self, track_name):
        query = 'MATCH (album:album)-[:containstrack]->(:track {name:"%s"}) RETURN album.name' %(track_name)
        result = self.graph.query(query)
        process_result_set(result)
        result.pretty_print()

    def get_artist_by_track(self, track_name):
        query = 'MATCH (artist:artist)-[:hastrack]->(:track {name:"%s"}) RETURN artist.name' %(track_name)
        result = self.graph.query(query)
        process_result_set(result)
        result.pretty_print()

    def get_album_art_url_from_track(self, track_name):
        query = 'MATCH (album:album)-[:containstrack]->(:track {name:"%s"}) RETURN album.art_url' %(track_name)
        result = self.graph.query(query)
        process_result_set(result)
        try:
            subset = result.result_set[-1]
            art_url = subset[0]
            display_art.display_art(art_url)
        except IndexError:
            print("No song found")


class Update:
    def __init__(self):
        self.meta_dict = process_metadata.get_meta_dict()

    def updateTrackNodes(self):
        CreateTrackNode(self.meta_dict).create_track_node()

    def updateArtistNode(self):
        CreateArtistNode(self.meta_dict).create_artist_node()

    def updateAlbumNode(self):
        CreateAlbumNode(self.meta_dict).create_album_node()

    def updateTrackEdges(self):
        createTrackEdge(self.meta_dict).create_artist_edge()
        createTrackEdge(self.meta_dict).create_album_edge()

    def updateArtistEdges(self):
        createArtistEdge(self.meta_dict).create_album_edge()
        createArtistEdge(self.meta_dict).create_track_edge()

    def updateAlbumEdges(self):
        createAlbumEdge(self.meta_dict).create_artist_edge()
        createAlbumEdge(self.meta_dict).create_track_edge()

    def update_all_nodes(self):
        self.updateAlbumNode()
        self.updateArtistNode()
        self.updateTrackNodes()

    def update_all_edges(self):
        self.updateTrackEdges()
        self.updateArtistEdges()
        self.updateAlbumEdges()

    def updateDgraph(self):
        add_edges_digraph()
        add_nodes_digraph()


def help():
    print("Fetch all song metadata - GET songs")
    print("Fetch all album metadata - GET albums")
    print("Fetch all artist metadata - GET artist")
    print("Fetch all songs by artist - GET tracks by artist")
    print("Fetch all songs by album - GET tracks by album")
    print("Fetch album by track - GET album by track")
    print("Fetch artist by track - GET artist by track")
    print("Fetch all albums by an artist - GET albums by artist")
    print("Fetch artist by album - GET artist by album")
    print("Create graph.svg file - show graph")

def driver_func(inp):
    if inp.strip().lower() == "get songs":
        queryFacade().get_songs()
    elif inp.strip().lower() == "get artists":
        queryFacade().get_artists()
    elif inp.strip().lower() == "get albums":
        queryFacade().get_albums()
    elif inp.strip().lower() == "open album art":
        track_name = input(">>> Enter Track Name: ")
        queryFacade().get_album_art_url_from_track(track_name)
    elif inp.strip().lower() == "get tracks by artist":
        artist_name = input(">>> Enter Artist Name: ")
        queryFacade().get_tracks_by_artist(artist_name)
    elif inp.strip().lower() == "get tracks by album":
        album_name = input(">>> Enter Album Name: ")
        queryFacade().get_tracks_by_album(album_name)
    elif inp.strip().lower() == "get albums by artist":
        artist_name = input(">>> Enter Artist Name: ")
        queryFacade().get_albums_by_artist(artist_name)
    elif inp.strip().lower() == "get artist by album":
        album_name = input(">>> Enter Album Name: ")
        queryFacade().get_artist_by_album(album_name)
    elif inp.strip().lower() == "get artist by track":
        track_name = input(">>> Enter Track Name: ")
        queryFacade().get_artist_by_track(track_name)
    elif inp.strip().lower() == "get album by track":
        track_name = input(">>> Enter Track Name: ")
        queryFacade().get_album_by_track(track_name)
    elif inp.strip() == "update":
        update_obj = Update()
        update_obj.update_all_nodes()
        update_obj.update_all_edges()
        update_obj.updateDgraph()
    else:
        print("Invalid command. Please try again.")


print("Type help to get information about commands")
print("Type exit to quit")
while True:
    query = input(">>> ")
    if query=="help":
        help()
    elif query=="exit":
        break
    elif query=="update":
        reload(process_metadata)
        driver_func("update")
    elif query=="show graph":
        f = open('graph.svg', 'w')
        f.write(spotify_graph.pipe().decode('utf-8'))
        f.close()
    else:
        driver_func(query)

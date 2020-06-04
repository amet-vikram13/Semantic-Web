from redis_proxy import get_connection
from redisgraph import Graph


# Create a graph. Redis takes care if it's already present.
def create_graph():
   redis_connection = get_connection() 
   graph = Graph('spotify', redis_connection)
   return graph

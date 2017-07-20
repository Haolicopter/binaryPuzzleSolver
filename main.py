import falcon
from Play import Play

app = falcon.API()
app.add_route('/', Play())

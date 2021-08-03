from meinheld import server
from flaskr import create_app

if __name__ == '__main__':
    server.listen(("0.0.0.0", 5000))
    server.run(app)

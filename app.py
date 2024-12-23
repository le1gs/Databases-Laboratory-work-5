
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb+srv://<username>:<password>@cluster.mongodb.net/')
db = client['movie_catalog']
movies_collection = db['movies']
ratings_collection = db['ratings']
users_collection = db['users']

@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.json
    result = movies_collection.insert_one(data)
    return jsonify({'message': 'Movie added', 'id': str(result.inserted_id)})

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = list(movies_collection.find({}, {'_id': 0}))
    return jsonify(movies)

@app.route('/movies/<string:title>', methods=['PUT'])
def update_movie(title):
    data = request.json
    result = movies_collection.update_one({'title': title}, {'$set': data})
    if result.matched_count > 0:
        return jsonify({'message': 'Movie updated'})
    return jsonify({'message': 'Movie not found'}), 404

@app.route('/movies/<string:title>', methods=['DELETE'])
def delete_movie(title):
    result = movies_collection.delete_one({'title': title})
    if result.deleted_count > 0:
        return jsonify({'message': 'Movie deleted'})
    return jsonify({'message': 'Movie not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
#db.create_all() #HAS TO BE RUN JUST ONCE. RUNNING THIS AGAIN WILL RESULT IN REINITIALIZED DATABASE


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"


video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, required=True, help="Did not send Name of the Video argument"
)
video_put_args.add_argument(
    "views", type=int, required=True, help="Did not send Views on the Video argument"
)
video_put_args.add_argument(
    "likes", type=int, required=True, help="Did not send Likes on the Video argument"
)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    "name", type=str, help="Did not send Name of the Video argument"
)
video_update_args.add_argument(
    "views", type=int, help="Did not send Views on the Video argument"
)
video_update_args.add_argument(
    "likes", type=int, help="Did not send Likes on the Video argument"
)

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}


class Video(Resource):
    

    # READ METHOD

    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with that ID")
        return result

    # CREATE METHOD

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video ID already exists...")
        video = VideoModel(
            id=video_id, name=args["name"], views=args["views"], likes=args["likes"]
        )
        db.session.add(video)
        db.session.commit()
        return video, 201

    # UPDATE METHOD

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video Doesn't Exist, cannot update.")
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        
        return result


    # DELETE METHOD

    def delete(Self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return "", 204


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)

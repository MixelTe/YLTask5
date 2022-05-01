from datetime import datetime
from flask import jsonify
from flask_restful import reqparse, abort, Resource
from flask_jwt_simple import jwt_required, get_jwt_identity
from data import db_session
from data.jobs import Jobs
from data.users import User

Fields = ("id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished")

parser = reqparse.RequestParser()
parser.add_argument("team_leader", required=True, type=int)
parser.add_argument("job", required=True)
parser.add_argument("work_size", required=True, type=int)
parser.add_argument("collaborators", required=True)
parser.add_argument("start_date", required=True)
parser.add_argument("end_date", required=True)
parser.add_argument("is_finished", required=True)

parser_noreq = reqparse.RequestParser()
parser.add_argument("team_leader", type=int)
parser.add_argument("job")
parser.add_argument("work_size", type=int)
parser.add_argument("collaborators")
parser.add_argument("start_date")
parser.add_argument("end_date")
parser.add_argument("is_finished")


def get_job_or_abort(job_id):
    session = db_session.create_session()
    job: Jobs = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")
    return job, session


class JobsResource(Resource):
    def get(self, user_id):
        job, _ = get_job_or_abort(user_id)
        return jsonify(
            {
                'job': job.to_dict(only=Fields)
            }
        )

    @jwt_required
    def delete(self, user_id):
        job, session = get_job_or_abort(user_id)
        userId = get_jwt_identity()
        if (job.team_leader != userId and userId != 1):
            abort(403, message=f"Forbidden")
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    @jwt_required
    def put(self, user_id):
        args = parser_noreq.parse_args()
        job, session = get_job_or_abort(user_id)
        userId = get_jwt_identity()
        if (job.team_leader != userId and userId != 1):
            abort(403, message=f"Forbidden")
        try:
            if ("team_leader" in args):
                team_leader = args["team_leader"]
                if (not session.query(User).get(team_leader)):
                    abort(400, message=f"Leader does not exists")
                job.team_leader = int(team_leader)
            if ("job" in args):
                job.job = str(args["job"])
            if ("work_size" in args):
                job.work_size = int(args["work_size"])
            if ("collaborators" in args):
                collaborators = args["collaborators"]
                try:
                    for user in collaborators.split(","):
                        if (not session.query(User).get(user)):
                            abort(400, message=f'Collaborator with id "{user}" does not exists')
                    job.collaborators = str(collaborators)
                except Exception:
                    abort(400, message=f'Bad collaborators value')
            if ("start_date" in args):
                job.start_date = datetime.fromisoformat(str(args["start_date"]))
            if ("end_date" in args):
                job.end_date = datetime.fromisoformat(str(args["end_date"]))
            if ("is_finished" in args):
                job.is_finished = bool(args["is_finished"])

            session.commit()
        except Exception:
            return jsonify({'error': 'Bad request'})
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        return jsonify(
            {
                'jobs': [item.to_dict(only=Fields) for item in jobs]
            }
        )

    @jwt_required
    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        try:
            job = Jobs(
                team_leader=int(args["team_leader"]),
                job=str(args["job"]),
                work_size=int(args["work_size"]),
                collaborators=str(args["collaborators"]),
                start_date=datetime.fromisoformat(str(args["start_date"])),
                end_date=datetime.fromisoformat(str(args["end_date"])),
                is_finished=bool(args["is_finished"]),
            )

            if (not db_sess.query(User).get(job.team_leader)):
                abort(400, message=f"Leader does not exists")
            for user in job.collaborators.split(","):
                if (not db_sess.query(User).get(user)):
                    abort(400, message=f'Collaborator with id "{user}" does not exists')
            db_sess.add(job)
            db_sess.commit()
        except Exception:
            return jsonify({'error': 'Bad request'})
        return jsonify({'success': 'OK'})
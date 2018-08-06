import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request

from mnist import model


x = tf.placeholder("float", [None, 784])
sess = tf.Session()

# restore trained data
with tf.variable_scope("regression"):
    logits1, variables1 = model.regression(x)
    y1 = tf.nn.softmax(logits1)
saver = tf.train.Saver(variables1)
saver.restore(sess, "mnist/data/regression.ckpt")


with tf.variable_scope("convolutional"):
    keep_prob = tf.placeholder("float")
    logits2, variables2 = model.convolutional(x, keep_prob)
    y2 = tf.nn.softmax(logits2)
saver = tf.train.Saver(variables2)
saver.restore(sess, "mnist/data/convolutional.ckpt")


def regression(input):
    return sess.run(y1, feed_dict={x: input}).flatten().tolist()


def convolutional(input):
    return sess.run(y2, feed_dict={x: input, keep_prob: 1.0}).flatten().tolist()


# webapp
app = Flask(__name__)


@app.route('/api/mnist', methods=['POST'])
def mnist():
    input = ((255 - np.array(request.json, dtype=np.uint8)) / 255.0).reshape(1, 784)
    output1 = regression(input)
    output2 = convolutional(input)
    return jsonify(results=[output1, output2])


@app.route('/')
def main():
    return render_template('index.html')


from flask_restful import reqparse, abort, Api, Resource


parser = reqparse.RequestParser()
parser.add_argument('task')


jobs = {
    1: {'task': 'build an API'},
    2: {'task': '哈哈哈'},
    3: {'task': 'perfect!'},
}
newest_job_id = max(jobs)  # int


class JobEditor(Resource):
    def get(self, job_id):
        if job_id not in jobs:
            abort(404, message="Job {} doesn't exist".format(job_id))
        return jobs[job_id]

    def delete(self, job_id):
        if job_id not in jobs:
            abort(404, message="Job {} doesn't exist".format(job_id))
        del jobs[job_id]
        return '', 204

    def put(self, job_id):
        args = parser.parse_args()
        newest_job_id = max(newest_job_id, job_id)
        jobs[job_id] = {'task': args['task']}
        return task, 201


class JobList(Resource):
    """A list of all jobs, and lets you POST to add new jobs
    """
    def get(self):
        return jobs

    def post(self):
        args = parser.parse_args()
        job_id = self.get_next_job_id()
        jobs[job_id] = {'task': args['task']}
        return jobs[job_id], 201
	
    def get_next_job_id(self):
        newest_job_id += 1
        return newest_job_id
		
api = Api(app)
api.add_resource(JobList, '/api/job')
api.add_resource(JobEditor, '/api/job/<int:job_id>')


if __name__ == '__main__':
    app.run(debug=True)

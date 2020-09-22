import flask
from flask_restful import Api, Resource
import warnings
from flask import request
import datetime

#from Utils.py import processing_function
#from Utils.py import test_step 

app = flask.Flask(__name__)

api = Api(app)

warnings.simplefilter('ignore', DeprecationWarning)
warnings.simplefilter('ignore', UserWarning)
warnings.simplefilter('ignore', RuntimeWarning)

# Lets define our API with a few attributes. We want to define how the predictions are outputed (JSON vs CSV) and we want
# to define our post logic. Post means we are giving the api something, get means we are asking it for something.
class Api(Api):
    def __init__(self, *args, **kwargs):
        super(Api, self).__init__(*args, **kwargs)
        self.representations = {
            'application/json': self.output_json,
            'text/csv': self.output_csv,
            'application/csv': self.output_csv}

    @staticmethod
    @api.representation('application/json')
    def output_json(data, code, headers=None):
        try:
            resp = flask.make_response(data.to_json(orient='index'), code)
        except AttributeError:
            resp = flask.make_response(data, code)
        resp.headers.extend(headers or {})
        return resp

    @staticmethod
    @api.representation('application/csv')
    @api.representation('text/csv')
    def output_csv(data, code, headers=None):
        resp = flask.make_response(data.to_csv(), code)
        resp.headers.extend(headers or {
            "Content-DisposPredicition": 'attachment; filename="results.csv"'
        })
        return resp


class Invocations(Resource):
    @staticmethod
    def post():
        raw_data = flask.request.data.decode('utf-8')
        # You will potentially need to add addtional arguments here so that you can process your data. As it stands now
        # it is only feeding the raw csv that you pass to it. There are two(2) easy ways to do this processing. The first
        # is to just include that chunk of code here and let it all run here. This is messy, so I recommend the second way.
        # The second is to include a Utils file that handles all the processing for us and import the function here.
        # An example would look like this:
        processed_data = processing_function(raw_data)
        model = tf.saved_model.load(r'C:\Users\andrew.downs\Desktop\Analytics Summit Resources\My_new_saved_model')
        epochs = 5
        for epoch in range(EPOCHS):
            for (x_test, y_test) in processed_data:
                Utils.test_step(model, x_test, y_test)
        return (predictions, 200)

api.add_resource(Invocations, '/invocations')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

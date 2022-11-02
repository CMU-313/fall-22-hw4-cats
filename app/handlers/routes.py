import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"


    @app.route('/predict')
    def predict():
        #use entries from the query string here but could also use json
        school  = request.args.get('school ')
        reason = request.args.get('reason')
        failures = request.args.get('failures')
        activities = request.args.get('activities')
        higher  = request.args.get('higher')
        absences = request.args.get('absences')
        G1 = request.args.get('G1')
        G2 = request.args.get('G2')
        data = [[school],[reason],[failures],[activities],[higher],[absences],[G1],[G2]]
        query_df = pd.DataFrame({
            'school': pd.Series(school),
            'reason': pd.Series(reason),
            'failures': pd.Series(failures),
            'activities':pd.Series(activities),
            'higher':pd.Series(higher),
            'absences':pd.Series(absences),
            'G1':pd.Series(G1),
            'G2':pd.Series(G2)
            })
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        return jsonify(np.asscalar(prediction))

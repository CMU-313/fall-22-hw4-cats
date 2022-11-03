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
        school  = request.args.get('school')
        if school == None:
            return "The json was missing (a) field(s)!"
        if school != "GP" and school != "MS":
            return "Invalid field values were included in the request!"
        
        reason = request.args.get('reason')
        if reason == None:
            return "The json was missing (a) field(s)!"
        if reason != "home" and reason != "reputation" and reason != "course" and reason != "other":
            return "Invalid field values were included in the request!"
        
        failures = request.args.get('failures')
        if failures == None:
            return "The json was missing (a) field(s)!"
        if failures.isnumeric() == False or failures < 0 or failures > 4:
            return "Invalid field values were included in the request!"
        
        activities = request.args.get('activities')
        if activities == None:
            return "The json was missing (a) field(s)!"
        if isinstance(activities, bool) == False:
            return "Invalid field values were included in the request!"
        
        higher  = request.args.get('higher')
        if higher == None:
            return "The json was missing (a) field(s)!"
        if isinstance(higher, bool) == False:
            return "Invalid field values were included in the request!"
        
        absences = request.args.get('absences')
        if absences == None:
            return "The json was missing (a) field(s)!"
        if absences.isnumeric() == False or absences < 0 or absences > 93:
            return "Invalid field values were included in the request!"
        
        G1 = request.args.get('G1')
        if G1 == None:
            return "The json was missing (a) field(s)!"
        if G1.isnumeric() == False or G1 < 0 or G1 > 20:
            return "Invalid field values were included in the request!"
        
        G2 = request.args.get('G2')
        if G2 == None:
            return "The json was missing (a) field(s)!"
        if G2.isnumeric() == False or G2 < 0 or G2 > 20:
            return "Invalid field values were included in the request!"
        
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

import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os
import json


def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)
    

    @app.route('/')
    def hello():
        return "try the predict route it is great!"


    @app.route('/predict', methods=['GET', 'POST'])
    def predict():
        print("json: ", request.json)
        if request.json == {}:
            return "The json in the request is empty!",400
        
        #use entries from the query string here but could also use json
        try:
            school = request.json['school']
        except KeyError:
            return "The json was missing (a) field(s)!",400
        if school != "GP" and school != "MS":
            return "Invalid field values were included in the request!",400
        school_GP = 0
        school_MS = 0
        if school == "GP":
            school_GP = 1
        elif school == "MS":
            school_MS = 1
            
        
        try:
            reason = request.json['reason']
        except KeyError:
            return "The json was missing (a) field(s)!",400
        if reason != "home" and reason != "reputation" and reason != "course" and reason != "other":
            return "Invalid field values were included in the request!",400
        reason_home = 0
        reason_reputation = 0
        reason_course = 0
        reason_other = 0
        if reason == "home":
            reason_home = 1
        elif reason == "reputation":
            reason_reputation = 1
        elif reason == "course":
            reason_course = 1
        elif reason == "other":
            reason_other = 1
        
        try:
            failures = request.json['failures']
        except KeyError:
            return "The json was missing (a) field(s)!",400
        if isinstance(failures, int) == False or failures < 0 or failures > 4:
            return "Invalid field values were included in the request!",400
        
        try:
            activities = request.json['activities']
        except KeyError:
            return "The json was missing (a) field(s)!",400
        if str(activities) != "yes" and str(activities) != "no":
            return "Invalid field values were included in the request!",400
        activities_yes = 0
        activities_no = 0
        if activities == "yes":
            activities_yes = 1
        elif activities == "no":
            activities_no = 1
        
        try:
            higher  = request.json['higher']
        except KeyError:
            return "The json was missing (a) field(s)!",400
        if higher != "yes" and higher != "no":
            return "Invalid field values were included in the request!",400
        higher_yes = 0
        higher_no = 0
        if higher == "yes":
            higher_yes = 1
        elif higher == "no":
            higher_no = 1
        
        try:
            absences = request.json['absences']
        except KeyError:
            return "The json was missing (a) field(s)!",400
        if isinstance(absences, int) == False or absences < 0 or absences > 93:
            return "Invalid field values were included in the request!",400
        
        try:
            G1 = request.json['G1']
        except KeyError:
            return "The json was missing (a) field(s)!",400
        if isinstance(G1, int) == False or G1 < 0 or G1 > 20:
            return "Invalid field values were included in the request!", 400
        
        try:
            G2 = request.json['G2']
        except KeyError:
            return "The json was missing (a) field(s)!",400
        if isinstance(G2, int) == False or G2 < 0 or G2 > 20:
            return "Invalid field values were included in the request!",400
        
        data = [[school],[reason],[failures],[activities],[higher],[absences],[G1],[G2]]
        
        query_df = pd.DataFrame({
            'failures': pd.Series(failures),
            'absences':pd.Series(absences),
            'G1':pd.Series(G1),
            'G2':pd.Series(G2),
            'school_GP': pd.Series(school_GP),
            'school_MS': pd.Series(school_MS),
            'reason_course': pd.Series(reason_course),
            'reason_home': pd.Series(reason_home),
            'reason_other': pd.Series(reason_other),
            'reason_reputation': pd.Series(reason_reputation),
            'activities_no':pd.Series(activities_no),
            'activities_yes':pd.Series(activities_yes),
            'higher_no':pd.Series(higher_no),
            'higher_yes':pd.Series(higher_yes)
            })
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        d = {}
        d['G3'] = int(prediction[0])
        return jsonify(d)

    if __name__ == '__main__':
        clf = joblib.load('model.pkl')
        app.run(port=8080)
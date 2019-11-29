import pickle
import pandas as pd
from flask import Flask, abort, jsonify, request , current_app


#my_cosine_model = pickle.load(open('similarity_model.pkl', 'rb'))
#courseDf.= pd.read_pickle("catalog.pkl") 

def load_files():
    return pickle.load(open('similarity_model.pkl', 'rb')) ,  pd.read_pickle("catalog.pkl")


def get_course_from_index(index):
    return courseDf.loc[index,['Name','Number']].to_json(orient='columns')

def get_index_for_course(course):
    return courseDf[courseDf.Name == course].index.values[0]

def get_gened_for_attribute(sACP,sCS,sHUM,sNAT,sQR,sSBS):
    return courseDf[(courseDf["ACP"] == sACP ) & (courseDf["CS"] == sCS ) & (courseDf["HUM"] == sHUM ) & (courseDf["NAT"] == sNAT ) & (courseDf["QR"] == sQR ) & (courseDf["SBS"] == sSBS )][["Name","Number","GPA","Total Students"]].sort_values('GPA',ascending = False).head(5).to_json(orient='records')


app = Flask(__name__)

@app.route('/similar', endpoint = 'similar' , methods=['POST'])
@app.route('/gened', endpoint = 'gened' , methods=['POST'])
def similar():
    #all kinds of error checking should go here
    data = request.get_json(force=True)

    if request.endpoint == 'similar':
       #convert our json to a numpy array
       course_request = str(data['course']) 

       course_index = get_index_for_course(course_request)

       similar_courses = list(enumerate(my_cosine_model[course_index]))
       sorted_similar_courses = sorted(similar_courses,key=lambda x:x[1], reverse=True)

       cnt = 0
       jstr = '{ "result": ['
       for element in sorted_similar_courses:
#          if courseDf.loc[element[0],['Name']].values[0] == course_request:
#              continue
          if cnt < 5:
             jstr = jstr + get_course_from_index(element[0])+','
          else:
             jstr = jstr + get_course_from_index(element[0]) 
          cnt = cnt+1
          if cnt > 5:
             jstr = jstr + '] }'
             break
    elif request.endpoint == 'gened':
         
         sACP = str(data['ACP'])
         sCS = str(data['CS'])
         sHUM = str(data['HUM'])
         sNAT = str(data['NAT'])
         sQR = str(data['QR'])
         sSBS = str(data['SBS'])        
         jstr = '{ "result": ' + get_gened_for_attribute(sACP,sCS,sHUM,sNAT,sQR,sSBS) + '] }'
    else:
         jstr = "Not a valid Function"
      #return our reccomendation
    return jstr

if __name__ == '__main__':
    my_cosine_model , courseDf = load_files()
    print( courseDf.count())
    with app.app_context():
       app.run(host='0.0.0.0', port=80)

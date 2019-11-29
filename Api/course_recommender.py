import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def combine_features(row):
    try:
       return row["Subject"]+" "+row["Description"]+" "+row['Degree Attributes']+" "+row["Name"]
    except:
       print ("Error:", row )
  
if __name__== "__main__":

##Step 1: Read CSV File
   courseDf = pd.read_csv("uiuc-course-catalog.csv")
   GpaDf = pd.read_csv("GPA.csv")
   combineDf = pd.merge(courseDf,GpaDf,how='left',left_on=['Number'] , right_on=['Course'])
##Step 2: Identify Feature Column
   features = ['Subject','Description','Degree Attributes']
   attributes = ['ACP', 'CS' , 'HUM' , 'NAT' , 'QR' , 'SBS' ]

##Step 3: Create a column in courseDF which combines all selected features
   for feature in features:
      combineDf[feature] = combineDf[feature].fillna('')

   for attribute in attributes:
       combineDf[attribute] = combineDf[attribute].fillna('N/A')

   combineDf["combined_features"] = combineDf.apply(combine_features,axis=1)

##Step 4: Create count matrix from this new combined column
   cv = CountVectorizer()

   count_matrix = cv.fit_transform(combineDf["combined_features"])

##Step 5: Compute the Cosine Similarity based on the count_matrix
   cosine_sim = cosine_similarity(count_matrix) 

   finalCourse = combineDf[["Number","Name","ACP", "CS" , "HUM" , "NAT" , "QR" , "SBS" , "GPA" , "Total Students" ]] 
   print(finalCourse.head())

   finalCourse.to_pickle("catalog.pkl")

   pkl_filename = "similarity_model.pkl"
   with open(pkl_filename, 'wb') as file:
        pickle.dump(cosine_sim, file)

import fasttext
import argparse
import pandas as pd
import sys, random, fileinput 
import nltk
import string
from nltk.corpus import stopwords
import re
nltk.download('stopwords')
en_stopwords = stopwords.words('english')

def clean_text(text):
    try:
        text = text.lower()                                                   # Make text lowercase
        text = re.sub('\[.*?\]', '', text)                                    # Remove text in square brackets    
        text = re.sub('https?://\S+|www\.\S+', ' ', text)                      # Remove hyper links
        text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)       # Remove punctuation
        text = re.sub('\n', ' ', text)                                         # Remove New line character
        text = re.sub('\w*\d\w*', '', text)  # Remove words containing numbers
        result_text = remove_stop_words(text)
        return result_text
    except Exception as err:
        print(err)

def remove_stop_words(text): #Removes the STOP words from the text
    try:
        resultwords  = [word for word in re.split("\W+",text) if word not in en_stopwords]
        result = ' '.join(resultwords)
        return result
    except Exception as err:
        print(err)

def load_rating_prediction_model(model_file_path): #Load the ML model
    try:
        model = fasttext.load_model(model_file_path)
        print("Load the ML Model")
        return model
    except Exception as err:
        print(err)
    
        
def read_input_file(input_file): #Reading Input File
    try:
        print("Reading Input file")
        df = pd.read_csv(input_file)
        return df
    except Exception as err:
        print(err)
        
def write_output_file(output_file, result_df): #Write to the output File
    try:
        result_df.to_csv(output_file, index=False)
        print("Creating Output file")
    except Exception as err:
        print(err)
     
def predict_ratings(model, text, k_value): #This function is for predict the ratings 
    try:
        label = model.predict(text, k=3)
        print("Predict ratings using the ML model")
        return label
    except Exception as err:
        print(err)   
        
def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', action='store', default=False,
                            dest='input_file',
                            help='Input File Path ')
        parser.add_argument('-m', action='store', default=False,
                            dest='model_file',
                            help='Model File path')
        parser.add_argument('-o', action='store', default=False,
                            dest='output_file',
                            help='Output File Name')
        args = parser.parse_args()
        k_value = 3
        model = load_rating_prediction_model(args.model_file)
        df = read_input_file(args.input_file)
        df['CleanText'] = df['Reviews'].apply(clean_text)
        df['Model_Prediction'] = None
        for index, row in df.iterrows():
            predicted_value = predict_ratings(model, row['CleanText'], k_value)
            predicted_value = predicted_value[0][0]
            if(predicted_value == "__label__five"):
                predicted_value = 5
            elif(predicted_value == "__label__four"):
                predicted_value = 4
            elif(predicted_value == "__label__three"):
                predicted_value = 3
            elif(predicted_value == "__label__two"):
                predicted_value = 2
            elif(predicted_value == "__label__one"):
                predicted_value = 1
            elif(predicted_value == "__label__zerp"):
                predicted_value = 0
            row['Model_Prediction'] = predicted_value
        write_output_file(args.output_file, df)  
        print("Done")
    except Exception as err:
        print("""To use the file needs to Provide three parameters along with the cmd you are executing
                For example: python predict_reviews.py -i inputfile -m review_rating_model.bin -o outputfile 
                As it is understandable that -i is for Input File 
                -m is for Fasttext model file
                -o is for Output file name""")
        print(err)  
        
        
main()
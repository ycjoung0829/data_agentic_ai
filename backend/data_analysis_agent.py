from image_analysis import analyze_image
import pandas as pd 

class DataAnalysisAgent:
    def __init__(self):
        # create a pandas dataframe
        self.df = pd.DataFrame()

    def run_analysis(self, image):
        # Do some data analysis
        text = analyze_image(image)
        return "Data analysis result"
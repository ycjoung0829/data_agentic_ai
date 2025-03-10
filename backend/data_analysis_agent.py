from image_analysis import analyze_image
import pandas as pd 
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os 



class DataAnalysisAgent:
    def __init__(self):
        key = os.getenv('AZURE_SUBSCRIPTION_KEY')
        endpoint = os.getenv('AZURE_ENDPOINT') 
        self.computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))
        # create a pandas dataframe
        self.dataset = dict() # create a dictionary to store data
        self.dataset['image_name'] = []
        self.dataset['description'] = []
        # self.dataset['topic'] = []
        self.dataset['url'] = []
        self.dataset['uploaded_date'] = []
        self.result = None 
    
        
    def run_analysis(self, file):
        """
        _summary_: This function runs the data analysis agent on the image and returns the description of the image.
        _params_: image: str
        _returns_: str
        """
        with open(file, "rb") as f:
        # add description
            description_result = self.computervision_client.describe_image_in_stream(f)
            # tags_result = self.computervision_client.tag_image_in_stream(f)
            return description_result.captions[0].text #, [tag.name for tag in tags_result.tags]
        return ""
    
    def run_agent(self, folder_path, folder, timestamp):
        # Do some data analysis
        for file in folder:
            file_path = folder_path / file.filename
            print("file_path in agent:", file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            text = self.run_analysis(file_path)
            self.dataset['image_name'].append(file.filename)
            self.dataset['description'].append(text)
            self.dataset['url'].append(file_path)
            # self.dataset['topic'].append(tags)
            self.dataset['uploaded_date'].append(timestamp)
        self.result = pd.DataFrame(self.dataset)
        result_csv = folder_path / "result.csv"
        self.result.to_csv(result_csv)
        # return self.result 
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes, Details
from msrest.authentication import CognitiveServicesCredentials
import os 

key = os.getenv('AZURE_SUBSCRIPTION_KEY')
endpoint = os.getenv('AZURE_ENDPOINT') 

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

def analyze_image(image):
    with open(image, "rb") as image:
        # add description
        description_result = computervision_client.describe_image_in_stream(image)
        return description_result.captions[0].text

if __name__ == "__main__":
    pass
import csv
import os 
from openai import OpenAI 
import pandas as pd 
import json 


class DataSchemaAgent:
    def __init__(self):
        self.dataset = pd.read_csv("uploaded_images/result.csv")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.openai_api_key)

    def extract_categories(self):
        """
        _summary_: This function extracts the categories from all image descriptions.
        _params_: descriptions: pandas dataframe
        _returns_: str
        """
        self.dataset = pd.read_csv("uploaded_images/result.csv")
        system_prompt = """You are a data schema agent whose task is to generate the categories that best classify the dataset.\
            The output format should be a dictionary where the key is the category name and the value is a list of the most relevant image name for that category."""
        prompt = "Generate the most relevant categories given the dataset with image name and descriptions."
        description_string = self.dataset[["image_name", "description"]].to_string(index=False) 
        print("description_string:", description_string)
        prompt += "The following is the dataset with image name and description\n" + description_string
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature = 0.2
        )
        print("content:",response.choices[0].message.content[len("   python"):-len("```")].strip())
        return json.loads(response.choices[0].message.content[len("   python"):-len("```")].strip())
    
    def run_agent(self):
        extracted_data = self.extract_categories()
        for category, images in extracted_data.items():
            for image in images:
                self.dataset.loc[self.dataset["image_name"] == image, "category"] = category
        self.dataset.to_csv("uploaded_images/result.csv", index=False)
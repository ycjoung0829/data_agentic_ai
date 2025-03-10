import csv
import os 
import openai 
import pandas as pd 
import json 


class DataSchemaAgent:
    def __init__(self):
        self.dataset = pd.read_csv("uploaded_images/result.csv")

    def extract_categories(self):
        """
        _summary_: This function extracts the categories from all image descriptions.
        _params_: descriptions: pandas dataframe
        _returns_: str
        """
        system_prompt = """You are a data schema agent whose task is to generate the most relevant categories that best classify the dataset given a dataset with image descriptions.\
            The output format should be a dictionary where the key is the category name and the value is a list of the most relevant image name for that category."""
        prompt = "Extract the most relevant categories that best classify the dataset with image name and descriptions."
        description_string = self.dataset[["image_name", "description"]].to_string(index=False) 
        print("description_string:", description_string)
        prompt += "The following is the dataset with image name and descr" + description_string
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature = 0.2
        )
        print(response.choices[0].message.parsed)
        return json.loads(response.choices[0].message.parsed)
from datasets import Dataset
import os

def to_hugging_faces(beginning_path : str, paths : list[str], status : int) -> Dataset :
    """
    @params
        paths: path to files to convert in dataset
        status: the status of the dataset generated or not
            warning in case of dataset that contains generated and non-generated
            modify the function

    @returns
        A Hugging Faces Dataset associating each file to its label
    """
    dict_dataset = {}
    for path in paths:
        f = open(beginning_path + path, "r")
        f_content = f.read()
        if ("program" in dict_dataset.keys()):
            dict_dataset["program"].append(f_content)
        else:
            dict_dataset["program"] = [f_content]
        if ("is_generated" in dict_dataset.keys()):
            dict_dataset["is_generated"].append(str(status))
        else:
            dict_dataset["is_generated"] = [(str(status))]
    return Dataset.from_dict(dict_dataset)

beginning_path = 'FormAI/DATASET/'
paths = os.listdir(beginning_path)
to_hugging_faces(beginning_path, paths, 1)

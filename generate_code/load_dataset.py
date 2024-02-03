from pathlib import Path
import json

def load_dataset(lang : str, part : str, buffer_size : int):
    """
    @params:
        lang: string of the language from which the question will be taken
        part: which part of the dataset dev/train/test
        buffer_size: the size of lines (pair code/question) that the function
            will return
    """
    path_q = Path(f'{lang}/{part}/{part}.question')
    path_c = Path(f'{lang}/{part}/{part}.code')
    res = {"question" : [], "code" : [], "lang": lang}
    with open(path_q, 'r') as f_q:
        with open(path_c, 'r') as f_c:
            for i in range(buffer_size):
                question = f_q.readline()
                code = f_c.readline()
                res["question"].append(question)
                res["code"].append(code)
    return res

#json = load_dataset("python", "dev", 20)
#print(json)

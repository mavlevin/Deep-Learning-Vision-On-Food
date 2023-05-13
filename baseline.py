import numpy as np
from tqdm import tqdm

class RandomUniformDistClassifier():
    def __init__(self):
        pass

    def train(self, img_data_list):
        pass
    
    def classify(self, img_path):
        possible_ratings = np.arange(0, 5.5, 0.5)
        return np.random.choice(possible_ratings)
    
class RandomMatchingDistClassifier():
    def __init__(self):
        pass   

    def train(self, img_data_list):
        self.ratings = [img_data[2] for img_data in img_data_list]

    def classify(self, img_path):
        return np.random.choice(self.ratings)

def test_accuracy(training_img_data, testing_img_data):
    rud = RandomUniformDistClassifier()
    rud.train(training_img_data)

    rmd = RandomMatchingDistClassifier()
    rmd.train(training_img_data)

    rud_correct = 0
    rmd_correct = 0
    total = 0
    print("testing classifiers")
    for img_data in tqdm(testing_img_data):
        total += 1
        if rud.classify(img_data[0]) == img_data[2]:
            rud_correct += 1
        if rmd.classify(img_data[0]) == img_data[2]:
            rmd_correct += 1

    print(f"random uniform dist classifier accuracy:  {rud_correct}/{total} = {(rud_correct/total)*100}%")
    print(f"random matching dist classifier accuracy: {rmd_correct}/{total} = {(rmd_correct/total)*100}%")
        

def read_img_data_csv(fpath):
    data = open(fpath, "r").read()
    data = data.split("\n")[1:-1] # remove titles first line and blank last line
    data = [d.split(",") for d in data]
    data = [[d[0], d[1], float(d[2])] for d in data]
    return data

def main():
    train, test = read_img_data_csv("training_photo_data.csv"), read_img_data_csv("testing_photo_data.csv")
    test_accuracy(train, test)

if __name__ == "__main__":
    main()
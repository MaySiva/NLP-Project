import requests
import json

# Base class for dataset loaders
class DatasetLoader:
    def __init__(self, name, url, format):
        self.name = name
        self.url = url
        self.format = format
    
    def download(self, filename):
        response = requests.get(self.url)
        with open(filename, 'wb') as f:
            f.write(response.content)
    
    def load(self):
        # Determine the file extension to choose the correct loading method
        filename = f"{self.name}.{self.format}"
        self.download(filename)
        with open(filename, 'r') as f:
            match self.format:
                case 'json':
                    return json.load(f)
                case 'jsonl':
                    dataset = []
                    for line in f:
                        dataset.append(json.loads(line))
                    return dataset
                case _:
                    raise 
    def parse(self):
        """Method to load and return dataset in a unified format"""
        raise NotImplementedError("Subclasses should implement this method.")


####################################################################################
class SQuADLoader(DatasetLoader):
    def parse(self):        
        data = self.load()
        # TODO: IMPLEMENT HERE


class HotpotQALoader(DatasetLoader):
    def parse(self):
        data = self.load()
        # TODO: IMPLEMENT HERE

class GSM8KLoader(DatasetLoader):
    def parse(self):
        data = self.load()
        # TODO: IMPLEMENT HERE

####################################################################################


class DatasetManager:
    def __init__(self):
        self.loaders = []

    def register_loader(self, loader):
        self.loaders.append(loader)

    def load_all_datasets(self):
        all_datasets = []
        for loader in self.loaders:
            all_datasets += loader.parse()
        return all_datasets
    


if __name__ == "__main__":
    # Initialize manager
    manager = DatasetManager()
    
    # Register dataset loaders
    manager.register_loader(SQuADLoader("squad_v2.0",
                                        "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json",
                                        'json'))
    manager.register_loader(HotpotQALoader("hotpotqa",
                                           "https://hotpotqa.github.io/hotpot_train_v1.1.json"),
                                            'json')
    
    # Load all datasets
    all_datasets = manager.load_all_datasets()
    print(f"Loaded {len(all_datasets)} items across all datasets.")
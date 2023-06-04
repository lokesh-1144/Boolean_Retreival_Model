

## Requirements

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install the requirements. Update apt if you are using EC2 Ubuntu instance.

```bash
sudo apt-get update
sudo apt install python3-pip -y
pip3 install tqdm Flask nltk
```

## Files and Tasks

1. `run_project.py` is the driver file, which will create the Flask app. Implement the logic for getting the postings list, executing DAAT AND query, merging linked list. etc. in this file.
2. `indexer.py` contains code to create and manipulate the index. Implement the necessary functions in indexer.
3. `preprocessor.py` contains code to pre-process documents & queries. Implement the necessary functions in preprocessor.
3. `linkedlist.py` defines the basic data structures for the postings list and the nodes of the postings list. It also contains code to manipulate the postings list. . Implement the necessary functions in linkedlist.
4. Execute `run_project.py` to create your index and start your API endpoint. Your endpoint will be available at `http://<ec2 public ipv4:9999>/execute_query`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

import os
import json
import logging

from .config import *

# set the logger ------------------------------------------------#
logger = logging.Logger(NAME)
logger.setLevel(LOGLEVEL)
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s - %(filename)s - %(lineno)d")
file_handler = logging.FileHandler(LOGFILE_ROUTES)
file_handler.setFormatter(file_formatter)

console_formatter = logging.Formatter("%(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)

handlers = {
    OUTPUT.FILE: [file_handler],
    OUTPUT.CONSOLE: [console_handler],
    OUTPUT.BOTH: [file_handler, console_handler]
}

for handler in handlers.get(LOGOUTPUT):
    logger.addHandler(handler)
# ---------------------------------------------------------------#

def read_data(train_data_dir, test_data_dir):
    '''parses data in given train and test data directories

    assumes:
    - the data in the input directories are .json files with
        keys 'users' and 'user_data'
    - the set of train set users is the same as the set of test set users

    Return:
        clients: list of client ids
        groups: list of group ids; empty list if none found
        train_data: dictionary of train data
        test_data: dictionary of test data
    '''
    clients = []
    groups = []
    train_data = {}
    test_data = {}

    train_files = os.listdir(train_data_dir)
    train_files = [f for f in train_files if f.endswith('.json')]
    for f in train_files:
        file_path = os.path.join(train_data_dir,f)
        with open(file_path, 'r') as inf:
            cdata = json.load(inf)
        clients.extend(cdata['users'])
        if 'hierarchies' in cdata:
            groups.extend(cdata['hierarchies'])
        train_data.update(cdata['user_data'])

    test_files = os.listdir(test_data_dir)
    test_files = [f for f in test_files if f.endswith('.json')]
    for f in test_files:
        file_path = os.path.join(test_data_dir,f)
        with open(file_path, 'r') as inf:
            cdata = json.load(inf)
        test_data.update(cdata['user_data'])

    clients = list(sorted(train_data.keys()))

    return clients, groups, train_data, test_data

if __name__ == "__main__":
    train_data_dir = "../data/femnist/train"
    test_data_dir = "../data/femnist/test"

    client, groups, train_data, test_data = read_data(train_data_dir, test_data_dir)

    logger.debug("client:" + str(client))
    logger.debug("groups:" + str(groups))
    logger.debug("train_data:" + str(train_data))
    logger.debug("test_data:" + str(test_data))

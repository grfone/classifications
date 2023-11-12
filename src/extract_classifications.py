import os
import gdown
import zipfile
import json
import bz2
import pickle
from utils.from_copied_link_to_download_link import transform_link


def extract():
    # If the classifications_dictionary already exists, then exit this function.
    if os.path.exists('./results/classifications_dictionary.pklz'):
        return

    # Create resources folder
    if not os.path.exists('./results'):
        os.mkdir('results')

    # Download 'classifications.zip' file
    if not os.path.exists('./resources/classifications.zip'):
        print(f"Downloading 'classifications.zip' file")
        link_2_classifications = "https://drive.google.com/file/d/1VEmzKmS5VsMLwZc9F5HBDcSj4p8cOCim/view?usp=drive_link"
        gdown.download(transform_link(link_2_classifications), './resources/classifications.zip')

    # Check if the file has been already decompressed, but if not, decompress it now
    if not os.path.exists('./resources/classifications'):
        print("Decompressing 'classifications.zip' file")
        with zipfile.ZipFile('./resources/classifications.zip', 'r') as zip_ref:
            zip_ref.extractall('./resources')  # It automatically creates the folder 'classifications'

    print("Performing the classification")
    # Create a list with all the compounds (the 'pids' are the names of the jsons but without extension)
    names_with_extension = os.listdir('./resources/classifications')
    names_without_extension = [os.path.splitext(name)[0] for name in names_with_extension]

    # Read each .json and extract the relevant information to a dictionary called 'classifications'
    # The keys will be the pids of the compounds and the values a list with all possible classifications
    classifications = {}

    for compound_pid in names_without_extension:
        # Open a different json file with each iteration
        json_file_path = './resources/classifications' + '/' + str(compound_pid) + '.json'
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Create a dictionary entry for the compound we just opened
        classifications[compound_pid] = []

        # Add all possible classifications to each compound
        for key in ['kingdom', 'superclass', 'class', 'subclass', 'direct_parent']:
            if key in data:
                if data[key] is not None:
                    classifications[compound_pid].append(data[key]['name'])

        if 'alternative_parents' in data:
            if data['alternative_parents'] is not None:
                for parent in data['alternative_parents']:
                    classifications[compound_pid].append(parent['name'])

        if 'intermediate_nodes' in data:
            if data['intermediate_nodes'] is not None:
                for node in data['intermediate_nodes']:
                    classifications[compound_pid].append(node['name'])

        if 'ancestors' in data:
            if data['ancestors'] is not None:
                for ancestor in data['ancestors']:
                    # Don't add the ancestor if it's already part of the compound's classification list
                    if ancestor not in classifications[compound_pid]:
                        classifications[compound_pid].append(ancestor)

    # Save the dictionary with all the data in a file called 'related.pklz'
    print('Saving the dictionary')
    with bz2.BZ2File('./results/classifications_dictionary.pklz', 'wb') as f:
        pickle.dump(classifications, f)

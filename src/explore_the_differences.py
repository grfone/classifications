import os
import gdown
import json
import bz2
import pickle
from utils.from_copied_link_to_download_link import transform_link


def explore(compound_type):
    print("Looking at the similarities and differences between our and their data")

    # Download their classifications
    if not os.path.exists('./resources/smrt_classyfire.tsv'):
        print(f"Downloading 'smrt_classyfire.tsv' file")
        link_to_their_classes = "https://drive.google.com/file/d/1WuEZhuYkc5xrZ4KeFxRz93GLXnEUvmTx/view?usp=drive_link"
        gdown.download(transform_link(link_to_their_classes), './resources/smrt_classyfire.tsv')

    # Upload their data to a list of lists
    their_data = []
    with open('./resources/smrt_classyfire.tsv', 'r') as file:
        for line in file:
            # Split each line by the tab character to create a list
            row = line.strip().split('\t')
            their_data.append(row)

    # Create a list with the keys of the compounds of interest extracted from their data
    compounds_of_interest = []
    for row in their_data:
        if compound_type in row:
            compounds_of_interest.append(row[2])

    # Load our data dictionary with the classifications
    with bz2.BZ2File('./results/classifications_dictionary.pklz', 'rb') as f:
        classifications = pickle.load(f)

    # Extract the InChIKeys of our compounds of interest
    our_list_of_compounds_of_interest = []
    for compound_pid in classifications:
        if compound_type in classifications[compound_pid]:
            # Open a different json file with each iteration
            json_file_path = './resources/classifications' + '/' + str(compound_pid) + '.json'
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
            if 'inchikey' in data:
                our_list_of_compounds_of_interest.append(data['inchikey'].split('=')[1].split('-')[0])

    # Check the differences:
    in_our_but_not_in_theirs = set(our_list_of_compounds_of_interest) - set(compounds_of_interest)
    in_theirs_but_not_in_ours = set(compounds_of_interest) - set(our_list_of_compounds_of_interest)
    coincidences = len(set(compounds_of_interest) & set(our_list_of_compounds_of_interest))

    # Save the compounds that we found, but they didn't, into a file
    with open("./results/in_our_but_not_in_theirs.txt", "w") as f:
        for compound in in_our_but_not_in_theirs:
            f.write(str(compound) + "\n")

    # Save the compounds that they found, but we didn't, into a another file
    with open("./results/in_theirs_but_not_in_ours.txt", "w") as f:
        for compound in in_theirs_but_not_in_ours:
            f.write(str(compound) + "\n")

    print("Differences saved in: in_our_but_not_in_theirs.txt and in_theirs_but_not_in_ours.txt")

    print("Coincidences:", coincidences)





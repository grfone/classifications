import os
import gdown
import bz2
import pickle
from utils.from_copied_link_to_download_link import transform_link


def extract(compound_type):
    # If the compounds of interest have already been extracted, then exit this function.
    if os.path.exists('./results/descriptors_trialkylamines.pklz'):
        return

    # Download 'descriptors.pklz' file
    if not os.path.exists('./resources/descriptors.pklz'):
        print(f"Downloading 'descriptors.pklz' file")
        link_to_descriptors = "https://drive.google.com/file/d/1IAfOzhww4c1C1-02z2qw_qaWjDuR_l-g/view?usp=drive_link"
        gdown.download(transform_link(link_to_descriptors), './resources/descriptors.pklz')

    # Download 'fingerprints.pklz' file
    if not os.path.exists('./resources/fingerprints.pklz'):
        print(f"Downloading 'fingerprints.pklz' file")
        link_to_fingerprints = "https://drive.google.com/file/d/18tihLxfqeDV4xFJ7FdiQMPZgMB8IOFcW/view?usp=drive_link"
        gdown.download(transform_link(link_to_fingerprints), './resources/fingerprints.pklz')

    # Load the classifications dictionary
    with bz2.BZ2File('./results/classifications_dictionary.pklz', 'rb') as f:
        classifications = pickle.load(f)

    # Load the descriptors database
    with bz2.BZ2File('./resources/descriptors.pklz', 'rb') as f:
        descriptors = pickle.load(f)

    # Load the fingerprints database
    with bz2.BZ2File('./resources/fingerprints.pklz', 'rb') as f:
        fingerprints = pickle.load(f)

    # Create a list with the rows to drop in order to keep only the trialkylamines
    rows_to_drop = []
    for index, row in fingerprints.iterrows():
        compound_pid = str(int(row['pid']))
        if compound_pid not in classifications:
            rows_to_drop.append(index)
        elif compound_type not in classifications[compound_pid]:
            rows_to_drop.append(index)

    # Drop any compound that is not a trialkylamine
    descriptors.drop(rows_to_drop, inplace=True)
    fingerprints.drop(rows_to_drop, inplace=True)

    # Save the fingerprints_trialkylamines dataframe
    with bz2.BZ2File('./results/fingerprints_trialkylamines.pklz', 'wb') as f:
        pickle.dump(fingerprints, f)

    # Save the descriptors_trialkylamines dataframe
    with bz2.BZ2File('./results/descriptors_trialkylamines.pklz', 'wb') as f:
        pickle.dump(descriptors, f)

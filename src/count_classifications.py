import bz2
import pickle
import os


def count():
    # If the classifications have been already counted, then exit this function.
    if os.path.exists('./results/classifications_with_over_5000_appearances.txt'):
        return

    # Load the classifications dictionary
    with bz2.BZ2File('./results/classifications_dictionary.pklz', 'rb') as f:
        classifications_dictionary = pickle.load(f)

    # Count the number of times that each classification appears in the dictionary
    unique_classifications = {}
    for compound in classifications_dictionary:
        for classification in classifications_dictionary[compound]:
            if classification in unique_classifications:
                unique_classifications[classification] = unique_classifications[classification] + 1
            else:
                unique_classifications[classification] = 1

    # Order the compounds by the number of times they repeat in SMRT
    sorted_items = sorted(unique_classifications.items(), key=lambda item: item[1], reverse=True)

    # Create a txt file with the 30 most common compounds
    with open("./results/30_most_common_classifications.txt", "w") as file:
        for key, value in sorted_items[:30]:
            file.write(f"{key}: {value}\n")

    # Create a txt file with all the compounds that appear more than 5000 times in SMRT
    with open("./results/classifications_with_over_5000_appearances.txt", "w") as file:
        for item in sorted_items:
            if item[1] > 5000:
                file.write(f"{item[0]}: {item[1]}\n")

    print("A file with the most common classifications has been created in the 'results' folder")

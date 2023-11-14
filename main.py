from src import extract_classifications
from src import count_classifications
from src import extract_compounds_of_interest
from src import explore_the_differences


if __name__ == '__main__':
    extract_classifications.extract()
    count_classifications.count()
    extract_compounds_of_interest.extract('Trialkylamines')
    explore_the_differences.explore('Trialkylamines')

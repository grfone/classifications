from src import extract_classifications
from src import count_classifications
from src import extract_compounds_of_interest


if __name__ == '__main__':
    extract_classifications.extract()
    count_classifications.count()
    extract_compounds_of_interest.extract('Trialkylamines')

def transform_link(copied_link):
    """This function gets a link in the format that comes from Google Drive when you click share > copy link
    and transform it to a link that can be downloaded using the library gdown in python

    Parameters
    ----------
    copied_link : str
    This parameter is the link that gets copied to the clipboard when you click share > copy link on Google Drive.

    Returns
    ----------
    download_link : str
    This variable is the actual link that can downloaded with the library gdown.
    """

    important_part = copied_link.replace("https://drive.google.com/file/d/", "").replace("/view?usp=drive_link", "")
    download_link = f"https://drive.google.com/u/0/uc?id={important_part}&export=download"

    return download_link

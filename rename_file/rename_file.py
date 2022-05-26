def clean_text(string_to_clean: str) -> str:
    """
    Clean the given `str` of non-ASCII characters

    :param string_to_clean: String with foreign characters
    :return: String without foreign characters
    """
    encoded_string = string_to_clean.encode("ascii", "ignore")
    new_string = encoded_string.decode()
    return new_string


import os, sys

# .exe --> sys.executable, .py --> __file__
try:
    if sys.frozen or sys.importers:
        script_directory = os.path.dirname(sys.executable)
except AttributeError:
    script_directory = os.path.dirname(os.path.realpath(__file__))

duplicate_counter = 1
file_extension = input("Please enter the file extension\n"
                  "For example (mf4, dat, blf...)\n"
                  ">")

with os.scandir(script_directory) as it:
    for entry in it:
        if entry.is_file() and entry.name.endswith("." + file_extension):
            original_file_name = entry.name[:]
            cleaned_file_name = clean_text(original_file_name)
            if cleaned_file_name != original_file_name:
                if os.path.isfile(clean_text(entry.path)) == 1:
                    duplicate_file_name = entry.path
                    while os.path.isfile(duplicate_file_name) == 1:
                        duplicate_file_name = (str(duplicate_counter) + "_" + cleaned_file_name)
                        duplicate_counter += 1
                    os.rename(original_file_name, duplicate_file_name)
                else:
                    os.rename(original_file_name, cleaned_file_name)
                    duplicate_counter = 1

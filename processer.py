# Import libraries
from ast import arg
from operator import neg
import pandas as pd
import posixpath,ntpath,json,platform,argparse
from datetime import datetime, timedelta


def time_to_float(time):
    """
        This function converts time to float.
        time(str): string value to convert to float.
    """
    time = str(time)
    if time=="nan":
        return 0
    try:
        (hours_, min_, sec_) = tuple(time.split(":"))
        hour_ = int(hours_)
        min_ = int(min_)
        sec_ = int(sec_)
        return hour_ * 3600 + min_ * 60 + sec_
    except Exception as e:
        print(f"Error {e} occured for {time}")

def determine_customer_reaction(all_data):
    """
        This function determines the customer's reaction, reactions are categoried into
        positive("Love","Care"), negative("Sad","Angry") and neutral("Wow","Haha").
        all_data(dataframe): a pandas dataframe that at least the following columns 
        ["Love","Care","Sad","Angry","Wow","Haha"].
    """
    positive = sum([int(all_data[each_pos]) for each_pos in customer_reaction_["positive"]])
    negative = sum([int(all_data[each_pos]) for each_pos in customer_reaction_["negative"]])
    neutral = sum([int(all_data[each_pos]) for each_pos in customer_reaction_["neutral"]])
    pd_frame = pd.Series([positive,negative,neutral], index=[["positive","negative","neutral"]])

    reaction = pd_frame[pd_frame==pd_frame.max()].index[0][0]
    data_map = [reaction]
    return pd.Series(data_map, index=["customer_reaction"])

def determine_content_type(all_data):
    """
        This function determines the content's type, contents  are categoried into
        general_knowledge(messages that contains words related to entertainment and general information), 
        science_nd_religion(messages that contains words related to science and religion),
        politics(messages that contains words related to politics) and
        peace_nd_violence(messages that contains words related to peace and violence).
        all_data(dataframe): a pandas dataframe that at least the following columns 
        ["entertainment","science","religion","politics","environment_&_economy","peace","violence_&_crime"].
    """
    general_knowledge = sum([int(all_data[each_pos]) for each_pos in content_type_["general_knowledge"]])
    science_nd_religion = sum([int(all_data[each_pos]) for each_pos in content_type_["science_nd_religion"]])
    politics = sum([int(all_data[each_pos]) for each_pos in content_type_["politics"]])
    peace_nd_violence = sum([int(all_data[each_pos]) for each_pos in content_type_["peace_nd_violence"]])

    pd_frame = pd.Series([general_knowledge,science_nd_religion,politics,peace_nd_violence], index=[["general_knowledge","science_nd_religion","politics","peace_nd_violence"]])
    max_result = pd_frame[pd_frame==pd_frame.max()]
    type_ = max_result.index[0][0]
    print(all_data["Message"],pd_frame,pd_frame.max(),type_,max_result[type_])
    data_map = [type_] if int(max_result[type_]) != 0 else ["no_label"]
    return pd.Series(data_map, index=["content_type"])

def convert_date_standard(input_date,format='%Y-%m-%d %H:%M:%S EDT'):
    """
    This function converts time to float.
    input_date(str): string value to convert to standard format.
    format(str): string value used to format input_date.
    """
    date_time_obj = None
    try:
        date_time_obj = datetime.strptime(input_date, format)
    except:
        try:
            date_time_obj = datetime.strptime(input_date, '%Y-%m-%d%H:%M:%S EDT')
        except:
            try:
                date_time_obj = datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S EST')
            except Exception as e:
                print(f"Error occured: {e} for {input_date}")
    return date_time_obj


# check if output file is .csv
def format_outfile_name(filename):
    assert type(filename) == type(" "), "format of filename should be string"
    return filename.split(".")[0]+".csv"

# function to handle user data path
def convert_path_for_win_linux(path_):
    if platform.machine() in ("arm64"):
        path_ = path_.replace(ntpath.sep,posixpath.sep)
    else:
        path_ = path_.replace(posixpath.sep,ntpath.sep)
    return path_

def open_json_files(file_name):
    assert ".json" in file_name, "File needs to be of type json"
    with open(file_name) as jsin_file:
        jsin_file_loaded = json.load(jsin_file)
    return jsin_file_loaded

# Read data
def label_present(all_data):
    """
        This function counts occurence of words to categories each message in one of the following
        ["entertainment","science","religion","politics","environment_&_economy","peace","violence_&_crime"],
        words related to this categories can be found in `signal_categories.json.
        all_data(dataframe): a pandas dataframe that at least the following columns 
        ["entertainment","science","religion","politics","environment_&_economy","peace","violence_&_crime"].
    """
    label_template_copy = label_template.copy()
    data = all_data["Message"]
    data = str(data)
    signal_categories_keys_ = list(label_template_copy.keys())
    signal_categories_keys_.sort()

    for each_cat in signal_categories_keys_:
        for each_signal in labeller_[each_cat]:
            if each_signal in data:
                print(f"Key is {each_cat} and signal is {each_signal}")
                label_template_copy[each_cat] += 1
    # if sum(label_template.values())==0:
    #     label_template["general"] = 1
    # total_signals = sum([label_template[each_cat] for each_cat in signal_categories_keys_])
    # data_map = [1 if (label_template[each_cat]/total_signals) > 0.1 else 0 for each_cat in signal_categories_keys_]
    data_map = [label_template_copy[each_cat] for each_cat in signal_categories_keys_]
    return pd.Series(data_map, index=signal_categories_keys_)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('datapath', type=str, help="Path to data")
    parser.add_argument('--outputname', type=str, default="vice_data_with_signal_category.csv", help="Name to save processed data as")
    args = parser.parse_args()
    print()
    # Read JSON signal_categories file
    labeller_ = open_json_files("signal_categories.json")

    # Customer reaction data
    customer_reaction_ = open_json_files("customer_reaction.json")
    content_type_ = open_json_files("content_type.json")

    # Read JSON template file
    label_template = open_json_files("template.json")
    
    important_columns = ['Post Created', 'Video Share Status', 'Total Views', 
                     'Total Views For All Crossposts', 'Video Length', 
                     'Message', 'Link Text', 'Likes at Posting','Likes',
                     'Comments','Shares','Love','Wow','Haha','Sad', 'Angry', 
                     'Care']
    file_name = args.datapath
    outputname = format_outfile_name(args.outputname)

    file_name = convert_path_for_win_linux(file_name)
    vice_data = pd.read_csv(file_name)[important_columns].reindex()
    vice_data['Post Created'] = vice_data[['Post Created']].applymap(convert_date_standard)
    vice_data['Video Length'] = vice_data[['Video Length']].applymap(time_to_float)
    vice_data2 = vice_data.apply(label_present,axis=1).reindex()
    vice_data = pd.concat([vice_data, vice_data2], axis=1)
    vice_data3 = vice_data.apply(determine_customer_reaction,axis=1).reindex()
    vice_data = pd.concat([vice_data, vice_data3], axis=1)
    vice_data4 = vice_data.apply(determine_content_type,axis=1).reindex()
    vice_data = pd.concat([vice_data, vice_data4], axis=1)
    vice_data.to_csv(outputname)
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

import argparse
import os
from azureml.core import Run, Dataset
from azureml.studio.core.io.data_frame_directory import save_data_frame_to_directory


def get_dict(dict_str):
    pairs = dict_str.strip("{}").split(";")
    new_dict = {}
    for pair in pairs:
        key, value = pair.strip().split(":")
        new_dict[key.strip().strip("'")] = value.strip().strip("'")

    return new_dict


print("Cleans the input data")

parser = argparse.ArgumentParser()
parser.add_argument("--raw_data", type=str, help="raw data")
parser.add_argument("--output_cleanse", type=str, help="cleaned taxi data directory")
parser.add_argument("--useful_columns", type=str, help="useful columns to keep")
parser.add_argument("--columns", type=str, help="rename column pattern")

args = parser.parse_args()

print("Argument 1(raw data id): %s" % args.raw_data)
print("Argument 2(columns to keep): %s" % str(args.useful_columns.strip("[]").split(";")))
print("Argument 3(columns renaming mapping): %s" % str(args.columns.strip("{}").split(";")))
print("Argument 4(output cleansed taxi data path): %s" % args.output_cleanse)

run = Run.get_context()
raw_data = Dataset.get_by_id(run.experiment.workspace, id=args.raw_data)

# These functions ensure that null data is removed from the dataset,
# which will help increase machine learning model accuracy.

useful_columns = [s.strip().strip("'") for s in args.useful_columns.strip("[]").split(";")]
columns = get_dict(args.columns)

new_df = (raw_data.to_pandas_dataframe()
          .dropna(how='all')
          .rename(columns=columns))[useful_columns]

new_df.reset_index(inplace=True, drop=True)

if not (args.output_cleanse is None):
    os.makedirs(args.output_cleanse, exist_ok=True)
    print("%s created" % args.output_cleanse)
    save_data_frame_to_directory(args.output_cleanse, new_df)
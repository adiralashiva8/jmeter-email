import os
import math
import time
import logging
import pandas as pd
from datetime import datetime
from datetime import timedelta


def generate_report(opts):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # URL or filepath of your company logo
    logo = opts.logo

    # input directory
    path = os.path.abspath(os.path.expanduser(opts.path))

    # files
    output_names = []
    if ( opts.output == "*.jtl" or opts.output == "*.csv"):
        for item in os.listdir(path):
            if os.path.isfile(item) and item.endswith('.jtl'):
                output_names.append(item)
            elif os.path.isfile(item) and item.endswith('.csv'):
                output_names.append(item)
    else:
        for curr_name in opts.output.split(","):
            curr_path = os.path.join(path, curr_name)
            output_names.append(curr_path)

    required_files = list(output_names)
    missing_files = [filename for filename in required_files if not os.path.exists(filename)]
    if missing_files:
        exit("Jmeter results file is missing: {}".format(", ".join(missing_files)))

    # Read result.jtl file
    df_from_each_file = (pd.read_csv(f, sep=opts.seperator) for f in output_names)
    df = pd.concat(df_from_each_file, ignore_index=True)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # jtl file validation part
    try:
        df[['label', 'success', 'elapsed', 'failureMessage', 'responseCode', 'threadName']]
    except Exception:
        exit("Error: Missing one of the required columns in file")

    total_count = df[['success']].count().values

    if total_count == 0:
        exit("Error: Invalid file, Please retry with valid file")

    # actual flow
    logging.info(" Capturing required data. This may take few minutes...")

    pass_count, fail_count, error_perct = 0, 0, 0

    for item in df[['success']].values.tolist():
        if item[0]:
            pass_count = pass_count + 1
        else:
            fail_count = fail_count + 1

    try:
        error_perct = float(fail_count) / float(total_count) * 100
    except ZeroDivisionError:
        error_perct = 0
    error_perct = round(error_perct, 2)
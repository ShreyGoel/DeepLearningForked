import pandas
import sqlite3
import os
import logging
from argparse import ArgumentParser

def build_parser():
    parser = ArgumentParser()
    parser.add_argument("--input", dest="input", help="input CSV file path", default="database/Data.csv")
    parser.add_argument("--output", dest="output", help="output SQLite DB file path", default="database/Data.db")
    return parser

def main():
    logging.basicConfig(level=logging.INFO)

    parser = build_parser()
    options = parser.parse_args()

    path_csv = options.input
    path_sqlite = options.output

    logging.info('Converting CSV to SQLite')
    logging.info('CSV Path=%s' % path_csv)
    logging.info('SQLite Path=%s' % path_sqlite)

    df_csv = pandas.read_csv(path_csv)
    logging.info('Finished reading CSV into dataframe. Dataframe preview:\n%s' % str(df_csv.head(5)))

    logging.info('Connecting to SQLite DB file')
    conn_write = sqlite3.connect(path_sqlite)    
    df_csv.to_sql('history', conn_write)
    logging.info('SQLite writing finished')

if __name__ == "__main__":
    main()

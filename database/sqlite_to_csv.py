import pandas
import sqlite3
import os
import logging
from argparse import ArgumentParser

def build_parser():
    parser = ArgumentParser()
    parser.add_argument("--input", dest="input", help="input SQLite DB file path", default="database/Data.db")
    parser.add_argument("--output", dest="output", help="output CSV file path", default="database/Data.csv")
    return parser

def main():
    logging.basicConfig(level=logging.INFO)

    parser = build_parser()
    options = parser.parse_args()

    path_sqlite = options.input
    path_csv = options.output

    logging.info('Converting SQLite to CSV')
    logging.info('SQLite Path=%s' % path_sqlite)
    logging.info('CSV Path=%s' % path_csv)

    conn_read = sqlite3.connect(path_sqlite)
    df_sqlite = pandas.read_sql_query('SELECT * FROM history;', conn_read)
    logging.info('Finished reading SQLite into dataframe. Dataframe preview:\n%s' % str(df_sqlite.head(5)))
    
    logging.info('Writing to CSV')
    df_sqlite.to_csv(path_csv, index=False)
    logging.info('CSV writing finished')

if __name__ == "__main__":
    main()

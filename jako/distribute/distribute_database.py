import time
from .distribute_utils import read_config, write_config
from .distribute_utils import add_experiment_id, add_timestamp
from .distribute_utils import fetch_latest_file
import sys


def get_db_object(self):
    config = self.config_data
    from ..database.database import Database

    machine_config = config['machines']
    db_config = config['database']
    username = db_config['DB_USERNAME']
    password = db_config['DB_PASSWORD']

    host_machine_id = int(db_config['DB_HOST_MACHINE_ID'])

    for machine in machine_config:
        if int(machine['machine_id']) == host_machine_id:
            host = machine['JAKO_IP_ADDRESS']
            break

    port = db_config['DB_PORT']
    database_name = db_config['DATABASE_NAME']
    db_type = db_config['DB_TYPE']
    table_name = db_config['DB_TABLE_NAME']
    encoding = db_config['DB_ENCODING']

    db = Database(username,
                  password,
                  host,
                  port,
                  database_name=database_name,
                  db_type=db_type,
                  table_name=table_name,
                  encoding=encoding)

    return db


def update_db(self, update_db_n_seconds, current_machine_id, stage):
    '''Make changes to the datastore based on a time interval

    Parameters
    ----------
    update_db_n_seconds | int | Time interval required to update the db

    Returns
    -------
    db | Database object | Database object with engine

    '''

    # update the database every n seconds
    db = get_db_object(self)
    config = self.config_data

    def __start_upload(results_data):

        if len(results_data) > 0:
            db_cols = db.return_columns()
            df_cols = results_data.columns
            missing_columns = [col for col in db_cols if col not in df_cols]
            new_columns = [col for col in df_cols if col not in db_cols]

            if len(missing_columns) > 0:
                exception_str = '''You have to change the experiment_name or
                add at least value for {}
                into the input parameter'''.format(missing_columns)
                raise Exception(exception_str)

            if len(new_columns) > 0:
                db.add_new_columns(new_columns)

            db.write_to_db(results_data)
        return db

    start_time = int(self.save_timestamp)

    start_row = 0
    end_row = 0

    while True:

        new_time = int(time.strftime('%D%H%M%S').replace('/', ''))

        if new_time - start_time >= update_db_n_seconds:

            if 'database' in config.keys():

                results_data = fetch_latest_file(self)

                if len(results_data) == 0:

                    start_time = new_time
                    time.sleep(update_db_n_seconds)
                    continue

                if len(results_data) > 0:
                    start_row = end_row
                    end_row = len(results_data)

                    if start_row != end_row and end_row > start_row:
                        results_data = add_timestamp(self, results_data)
                        results_data = add_experiment_id(self,
                                                         results_data,
                                                         current_machine_id,
                                                         start_row,
                                                         end_row,
                                                         db,
                                                         stage)

                        __start_upload(results_data)

                new_config = read_config(self)

                if 'finished_scan_run' in new_config.keys():

                    results_data = fetch_latest_file(self)

                    start_row = end_row
                    end_row = len(results_data)

                    if start_row != end_row and end_row > start_row:
                        results_data = add_timestamp(self, results_data)
                        results_data = add_experiment_id(self,
                                                         results_data,
                                                         current_machine_id,
                                                         start_row,
                                                         end_row,
                                                         db,
                                                         stage)

                        __start_upload(results_data)
                        write_config(self, new_config)

                    sys.exit()

                else:

                    start_time = new_time
                    time.sleep(update_db_n_seconds)

            else:
                print('Database credentials not given.')

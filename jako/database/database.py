from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, drop_database
from sqlalchemy.schema import DropTable


class Database:

    def __init__(self,
                 username=None,
                 password=None,
                 host=None,
                 port=None,
                 db_type='sqlite',
                 database_name='EXPERIMENT_LOG',
                 table_name='experiment_log',
                 encoding='LATIN1'):
        '''

        Parameters
        ----------
        username | str | The default is None.
        password | str | The default is None.
        host | str , optional| The default is None.
        port | str , optional| The default is None.
        db_type | str | The default is 'sqlite'.
        database_name | str | The default is 'EXPERIMENT_LOG'.
        table_name | str | The default is 'experiment_log'.

        Returns
        -------
        None.

        '''
        self.db_type = db_type
        self.database_name = database_name
        self.table_name = table_name
        self.encoding = encoding
        DB_URL = ''
        if db_type == 'sqlite':
            DB_URL = 'sqlite:///' + database_name + '.db'
        elif db_type == 'mysql':
            if port is None:
                port = 3306

            url = '''mysql+pymysql://{}:{}@{}:{}/{}'''.format(username,
                                                              password,
                                                              host,
                                                              str(port),
                                                              database_name)

            DB_URL = (url)

        elif db_type == 'postgres':
            if port is None:
                port = 5432

            url = 'postgresql://{}:{}@{}:{}/{}'.format(username,
                                                       password,
                                                       host,
                                                       str(port),
                                                       database_name)

            DB_URL = (url)

        self.DB_URL = DB_URL

    def create_db(self):
        '''
        Create database if it doesn't exists.
        '''

        engine = create_engine(self.DB_URL,
                               echo=False, isolation_level='AUTOCOMMIT')

        if not database_exists(engine.url):

            new_engine = create_engine(
                self.DB_URL.replace(self.database_name, ''),
                echo=False,
                isolation_level='AUTOCOMMIT',
            )
            conn = new_engine.connect()

            try:
                conn.execute(
                    '''
                    CREATE DATABASE {} ENCODING '{}'
                    '''.format(
                        self.database_name, self.encoding
                    )
                )

            except Exception as e:
                print(e)

        return engine

    def drop_db(self):
        '''
        Drop the database.
        '''
        drop_database(self.DB_URL)

    def delete_table(self, table_name):
        '''
        Delete the table.
        '''
        DropTable(table_name)

    def write_to_db(self, data_frame):
        '''


        Parameters
        ----------
        data_frame | `DataFrame` | DataFrame object consisting of tabular data.

        Returns
        -------
        None.

        '''
        engine = self.create_db()
        data_frame.to_sql(self.table_name, con=engine,
                          if_exists='append', index=False)

    def query_table(self, query):
        '''


        Parameters
        ----------
        query | `str`| Database query for the respective sql engine

        Returns
        -------
        res | `list` of `tuples` | Query output from the database

        '''
        engine = self.create_db()
        res = engine.execute(query).fetchall()
        return res

    def show_table_content(self):
        '''
        Returns
        -------
        res |`list` of `tuples` | Query output from the database

        '''
        res = self.query_table('SELECT * FROM {}'.format(self.table_name))
        return res

    def return_table_df(self):
        '''
        Returns
        -------
        data | Pandas DataFrame object | returns the database as a dataframe

        '''
        import pandas as pd

        table = self.show_table_content()
        data = pd.DataFrame(table)
        return data

    def return_existing_experiment_ids(self):
        '''
        Returns
        -------
        ids | Pandas Series object | returns the experiment id of the table

        '''

        query_str = 'SELECT experiment_id from {}'.format(self.table_name)
        res = self.query_table(query_str)
        res = [val[0] for val in res]

        return res

    def return_columns(self):
        '''
        Returns
        -------
        cols | list| returns the columns of the table
        '''

        query_string = """select COLUMN_NAME from information_schema.columns
                        where table_name='{}'"""
        query_string = query_string.format(self.table_name)
        cols = self.query_table(query_string)
        cols = [col[0] for col in cols]

        return cols

    def add_new_columns(self, columns):
        ''' Add a new column to the Database'''

        query_str = 'ALTER TABLE {}'.format(self.table_name)
        col_query_str = ' ADD COLUMN {} varchar,'

        for col in columns:
            query_str = query_str + col_query_str.format(col)

        query_str = query_str.rstrip(',') + ';'

        try:
            self.query_table(query_str)
        except Exception as e:
            exception_str1 = '''
                    This result object does not return rows.
                    '''
            exception_str2 = '(psycopg2.errors.DuplicateColumn)'
            exception_str3 = '(psycopg2.errors.UndefinedTable)'
            exceptions = [exception_str1, exception_str2, exception_str3]
            e = str(e)
            if any(ex in e for ex in exceptions):
                pass
            else:
                raise Exception(e)

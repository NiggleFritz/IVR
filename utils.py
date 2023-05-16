from google.cloud import bigquery

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_contacts_list_if_not_exists(project_id:str,
                                       dataset_id:str,
                                       table_id:str,
                                       source_file:str):
    bq_client = bigquery.Client()

    does_exist = check_if_table_exists(project_id=project_id,
                                       dataset_id=dataset_id,
                                       table_id=table_id,
                                       client=bq_client)

    if not does_exist:
        schema_list = [{"name":"phone_number","data_type":"STRING","mode":"NULLABLE"}]
        create_table_from_schema_file(project_id=project_id,
                                      dataset_id=dataset_id,
                                      table_id=table_id,
                                      schema_list=schema_list,
                                      client=bq_client)

def check_if_table_exists(project_id,
                          dataset_id,
                          table_id,
                          client):
    table_to_check_for = f'{project_id}.{dataset_id}.{table_id}'
    try:
        client.get_table(table_to_check_for)
        return True
    except Exception:
        return False

def get_contacts(contact_list):
    query = f'SELECT phone_number from `{contact_list}`'
    query_job = submit_query(query=query,
                             client=bigquery.Client())

def add_to_contacts(phone_number, contact_list):
    new_contact = {'phone_number':phone_number}
    query = f'''INSERT INTO `{contact_list}` (phone_number)
        VALUES ({new_contact['phone_number']})'''
    submit_query(query=query,
                 client=bigquery.Client())

def create_table_from_schema(project_id:str,
                             dataset_id:str,
                             table_id:str,
                             schema_list:list[{str:str}],
                             client:bigquery.Client) -> bigquery.Table:
    """ Creates a table at the given location

    This function will allow you to create a table in a given BigQuery dataset 
    from a provided schema. 

    Args:
        dataset_id: The name of the dataset to create the table in.

        table_id: The name of the table to create.

        schema: A list of dictionaries. Each dictionary is a new column i.e
        [{"name":"value","data_type":"STRING","mode":"REQUIRED"},
        {"name":"value","data_type":"INT64","mode":"NULLABLE"}]
    """
    bigquery_schema = build_schema_from_list(schema_list=schema_list)
    table_path = f"{project_id}.{dataset_id}.{table_id}"

    table = bigquery.Table(table_path,schema=bigquery_schema)

    try:
        table = client.create_table(table=table)
        logger.info(f"Table {table.table_id} created successfully")
        return table
    except Exception as error:
        exception_handler(error=error,
                         module='bigquery',
                         query=query)

# Querying BigQuery tables and views
def submit_query(
    query:str,
    client:bigquery.Client) -> bigquery.QueryJob:
    """ Submit a query job to BigQuery.

    Args:
    query: A string containing a BigQuery compatible SQL query
    client: A BigQuery client instance
    """
    logger.info("Submitting query to BigQuery:\n{query}\n")
    query_job = client.query(query)

    return query_job

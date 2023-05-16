import config
import utils

def setup():
    utils.create_contact_list_if_not_exists(project_id=config.PROJECT_ID,
                                            dataset_id=config.DATASET_ID,
                                            table_id='michaels_personal_contacts',
                                            source_file=config.SOURCE_FILE)

if __name__ == "__main__":
    setup()

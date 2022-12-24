"""
Template Component main class.

"""
import csv
import logging
from datetime import datetime
import mso_hapi as hapi

from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

# configuration variables
KEY_API_TOKEN = '#private_app_token'

# list of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = [KEY_API_TOKEN]


class Component(ComponentBase):
    """
        Extends base class for general Python components. Initializes the CommonInterface
        and performs configuration validation.

        For easier debugging the data folder is picked up by default from `../data` path,
        relative to working directory.

        If `debug` parameter is present in the `config.json`, the default logger is set to verbose DEBUG mode.
    """

    def __init__(self):
        super().__init__()

    def run(self):
        """
        Main execution code
        """

        # check for missing configuration parameters
        self.validate_configuration_parameters(REQUIRED_PARAMETERS)
        params = self.configuration.parameters
        # Access parameters in data/config.json
        # if params.get(KEY_PRINT_HELLO):
        #     logging.info("Hello World")

        # get last state data/in/state.json from previous run
        # previous_state = self.get_state_file()
        # logging.info(previous_state.get('some_state_parameter'))

        # Create output table (Tabledefinition - just metadata)
        table = self.create_out_table_definition('output.csv', incremental=True, primary_key=['id'])

        # get file path of the table (data/out/tables/Features.csv)
        out_table_path = table.full_path
        logging.info(out_table_path)

        # DO whatever and save into out_table_path
        token = params.get(KEY_API_TOKEN)
        hubspot_data = hapi.HubspotAPI(token)

        deals = hubspot_data.getDeals()

        out_file = csv.writer(open(table.full_path, mode="wt", encoding='utf-8', newline=''))
        out_file.writerow(["id", "amount", "dealname", "timestamp"])
        for deals in deals:
            out_file.writerow([deals["id"], 
                               deals["properties"]["amount"], 
                               deals["properties"]["dealname"], 
                               datetime.now().isoformat()])

        # with open(table.full_path, mode='wt', encoding='utf-8', newline='') as out_file:
        #     writer = csv.DictWriter(out_file, fieldnames=['timestamp'])
        #     writer.writeheader()
        #     writer.writerow({"timestamp": datetime.now().isoformat()})

        # Save table manifest (output.csv.manifest) from the tabledefinition
        self.write_manifest(table)

        # Write new state - will be available next run
        self.write_state_file({"some_state_parameter": "value"})


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)

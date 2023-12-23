from datatypes import readSources
from hqp_link_collector import update_data

sources = readSources()

# if it has been too long since update
# run update


update_data()

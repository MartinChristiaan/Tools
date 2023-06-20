from hqp_link_collector import update_data
from datatypes import readSources
sources = readSources()

# if it has been too long since update
# run update


update_data()

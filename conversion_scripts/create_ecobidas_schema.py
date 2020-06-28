import json
import os
import csv
from utils import define_activity_context, define_new_activity, get_item_info, define_new_item, define_response_choice, list_responses_options
# import pandas as pd
import warnings

'''
# This script takes the content of the a csv file and turns it into a reproschema
# protocol.
# This scripts loops through the items of the csv and creates a new reproschema
# activity with every new checklist "section" it encouters: this new activity
# will be added to the protocol.
# Every new item encountered is added to the current activity.
'''

'''
-----------------------------------------------------------------------------
                                  TO DO
-----------------------------------------------------------------------------

- automate the choice of from radio to dropdown menu if the number of
   response_choices goes above a certain number
- allow for several condition checks for visibility
- allow for mandatory items
'''

# -----------------------------------------------------------------------------
#                                   PARAMETERS
# -----------------------------------------------------------------------------
# modify the following lines to match your needs

REPRONIM_REPO = 'https://raw.githubusercontent.com/ReproNim/reproschema/master/'

# ----------------------------------------
# where the checklist csv is. It is in xlsx dir of this repo
# but it can also be downloaded from here:
# https://github.com/NeuroVault/NeuroVault/blob/master/xlsx/

# INPUT_FILE = '/home/remi/github/COBIDAS_chckls/xlsx/metadata_neurovault.csv'
# INPUT_FILE = '/home/remi/github/COBIDAS_chckls/xlsx/PET_guidelines.csv'
INPUT_FILE = '/home/remi/github/COBIDAS_chckls/xlsx/COBIDAS_MRI - clean.csv'

# ----------------------------------------
# where the files will be written on your machine: the local repository
# corresponding to the remote where of the reproschema will be hosted

OUTPUT_DIR = '/home/remi/github/COBIDAS_chckls'

# ----------------------------------------
# Placeholder to insert in all instances of the remote repo that will host the schema representation
# Most likely you just need to replace Remi-Gau in the following line by your github username

REMOTE_REPO = 'https://raw.githubusercontent.com/Remi-Gau/COBIDAS_chckls/'

# ----------------------------------------
# to which branch of reproschema the user interface will be pointed to
# In the end the cobidas-UI repository will be reading the schema from the URL that that
# starts with: REMOTE_REPO + BRANCH

# BRANCH = 'master'
# BRANCH = 'neurovault'
BRANCH = 'remi-MRI'

# ----------------------------------------
# Protocol name

# PROTOCOL = 'neurovault_'
PROTOCOL = 'PET_'
PROTOCOL = 'cobidas-MRI_'

INCLUDE_COL = []

# ----------------------------------------
# CSV column


# Neurovaut
# SECTION_COL = 1
# ITEM_COL = 2
# QUESTION_COL = 3
# RESPONSE_TYPE_COL = 4
# CHOICE_COL = 5
# MANDATORY_COL = 6
# VISIBILITY_COL = 7


# PET
# SECTION_COL = 4
# ITEM_COL = 5
# QUESTION_COL = 7
# RESPONSE_TYPE_COL = 9
# CHOICE_COL = 10
# MANDATORY_COL = 11
# VISIBILITY_COL = 12

# CSV_INFO = pd.DataFrame(
#     {'label': ['section', 'item', 'question', 'resp_type', 'choice', 'mandatory', 'vis'],
#     'col': [4, 5, 7, 9, 10, 11, 12]
#     }
# )

# COBIDAS MRI
INCLUDE_COL = 13
MANDATORY_COL = 15
SECTION_COL = 18
ITEM_COL = 24
QUESTION_COL = 26
RESPONSE_TYPE_COL = 28
CHOICE_COL = 29
VISIBILITY_COL = 30

# --------------------
# VERSION

VERSION = '0.0.1'

# -----------------------------------------------------------------------------
#                                   START
# -----------------------------------------------------------------------------

# protocol names
PROTOCOL_SCHEMA_FILE = PROTOCOL + 'schema'
PROTOCOL_CONTEXT_FILE = PROTOCOL + 'context'
PROTOCOL_DIR = PROTOCOL[0:-1]

# create output directories
if not os.path.exists(os.path.join(OUTPUT_DIR, 'protocols', PROTOCOL_DIR)):
    os.makedirs(os.path.join(OUTPUT_DIR, 'protocols', PROTOCOL_DIR))

# define the jsonld for the schema protocol
PROTOCOL_SCHEMA_JSON = {
    '@context': [REPRONIM_REPO + 'contexts/generic',
                 REMOTE_REPO + BRANCH + '/protocols/'
                 + PROTOCOL_DIR + '/'
                 + PROTOCOL_CONTEXT_FILE],
    '@type': 'reproschema:Protocol',
    '@id': PROTOCOL_SCHEMA_FILE,
    'prefLabel': PROTOCOL_SCHEMA_FILE,
    'schema:description': PROTOCOL_SCHEMA_FILE,
    'schema:schemaVersion': VERSION,
    'schema:version': VERSION,
    'landingPage': REMOTE_REPO + BRANCH + '/protocols/' + PROTOCOL_DIR + '/README.md',
    'ui': {
        'allow': ["autoAdvance", "allowExport"],
        'shuffle': False,
        'order': [],
        'addProperties': [],
    }
}

# define the jsonld for the context associated to this protocol
PROTOCOL_CONTEXT_JSON = {
    '@context': {
        '@version': 1.1,
        'activity_path': REMOTE_REPO + BRANCH + '/activities/',
    }
}

# Initiliaze this variable as we will need to check if we got to a new section while
# looping through items
section = ''

# loop through rows of the csv file and create corresponding jsonld for each item
with open(INPUT_FILE, 'r') as csvfile:
    PROTOCOL_METADATA = csv.reader(csvfile)
    for row in PROTOCOL_METADATA:

        item_name, question, response_type, response_choices, visibility = get_item_info(
                                                                            row,
                                                                            ITEM_COL,
                                                                            QUESTION_COL,
                                                                            RESPONSE_TYPE_COL,
                                                                            CHOICE_COL,
                                                                            VISIBILITY_COL,
                                                                            INCLUDE_COL)

        if item_name != []:

            # -------------------------------------------------------------------
            # detect if this is a new section if so it will create a new activity
            # -------------------------------------------------------------------
            if row[SECTION_COL] != section:

                # update section name
                section = row[SECTION_COL]

                # where the items of this section will be stored
                activity_dir = PROTOCOL + section

                # names of this section schema and its corresponding jsonld files
                activity_schema_name = PROTOCOL + section

                activity_schema_file = activity_schema_name + '_schema'

                activity_context_file = PROTOCOL + section + '_context'

                # create dir for this section
                if not os.path.exists(os.path.join(OUTPUT_DIR, 'activities',
                                                   activity_dir)):
                    os.makedirs(os.path.join(OUTPUT_DIR, 'activities',
                                             activity_dir))
                    os.makedirs(os.path.join(OUTPUT_DIR, 'activities',
                                             activity_dir, 'items'))

                activity_context_json, activity_at_context = define_activity_context(
                                                                REPRONIM_REPO,
                                                                REMOTE_REPO,
                                                                BRANCH, activity_dir,
                                                                activity_context_file)

                activity_schema_json = define_new_activity(
                                        activity_at_context,
                                        activity_schema_name,
                                        PROTOCOL, section, VERSION)

                # update the content of the protool schema and context wrt this new activity
                append_to_protocol = {
                    'variableName': activity_schema_name,
                    'isAbout': activity_schema_name,
                    # for the name displayed by the UI for this acivity we simply reuse the
                    # activity name
                    "prefLabel": {
                        "en": activity_schema_name.replace(PROTOCOL, "").replace("_", ": ").replace("-", " ")
                    }
                }

                PROTOCOL_SCHEMA_JSON['ui']['order'].append(activity_schema_name)
                PROTOCOL_SCHEMA_JSON['ui']['addProperties'].append(append_to_protocol)

                PROTOCOL_CONTEXT_JSON['@context'][activity_schema_name] = {
                    '@id': 'activity_path:' + activity_dir + '/' + activity_schema_file,
                    '@type': '@id'
                }

                print(activity_schema_name)

            # -------------------------------------------------------------------
            # update the content of the activity schema and context with new item
            # -------------------------------------------------------------------
            append_to_activity = {
                'variableName': item_name,
                'isAbout': item_name,
                "isVis": visibility
            }

            activity_schema_json['ui']['order'].append(item_name)
            activity_schema_json['ui']['addProperties'].append(append_to_activity)

            activity_context_json['@context'][item_name] = {
                '@id': 'item_path:' + item_name,
                '@type': '@id'
            }

            # save activity schema and context with every new item
            with open(os.path.join(OUTPUT_DIR, 'activities', activity_dir,
                                   activity_schema_file), 'w') as ff:
                json.dump(activity_schema_json, ff, sort_keys=False, indent=4)

            with open(os.path.join(OUTPUT_DIR, 'activities', activity_dir,
                                   activity_context_file), 'w') as ff:
                json.dump(activity_context_json, ff, sort_keys=False, indent=4)

            # -------------------------------------------------------------------
            # Create new item
            # -------------------------------------------------------------------
            print('   ' + item_name)

            if question == "":
                warnings.warn("No question for this item.", UserWarning)
            else:
                print('       ' + question)
            print('       ' + response_type)
            
            item_schema_json = define_new_item(activity_at_context, item_name, question, VERSION)

            inputType, responseOptions = define_response_choice(response_type, response_choices)

            item_schema_json['ui']['inputType'] = inputType
            item_schema_json['responseOptions'] = responseOptions

            # write item schema
            with open(os.path.join(
                OUTPUT_DIR, 'activities',
                activity_dir, 'items',
                    row[ITEM_COL]), 'w') as ff:

                json.dump(item_schema_json, ff, sort_keys=False, indent=4)

# write protocol jsonld
with open(os.path.join(OUTPUT_DIR, 'protocols', PROTOCOL_DIR,
                       PROTOCOL_SCHEMA_FILE), 'w') as ff:
    json.dump(PROTOCOL_SCHEMA_JSON, ff, sort_keys=False, indent=4)

with open(os.path.join(OUTPUT_DIR, 'protocols', PROTOCOL_DIR,
                       PROTOCOL_CONTEXT_FILE), 'w') as ff:
    json.dump(PROTOCOL_CONTEXT_JSON, ff, sort_keys=False, indent=4)

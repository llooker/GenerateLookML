from github import Github
from lookml import lookml, View, Dimension, DimensionGroup
import json
import os
import requests 


def schema_table_search(event, context):

    ## lookml configs
    lookml.DB_FIELD_DELIMITER_START = ''
    lookml.DB_FIELD_DELIMITER_END = ''
    lookml.INDENT = ' '*2
    lookml.NEWLINE = '\n'
    lookml.NEWLINEINDENT = ''.join([lookml.NEWLINE,lookml.INDENT])
    lookml.TIMEFRAMES = [ 'raw', 'year', 'quarter', 'month', 'week', 'date', 'day_of_week', 'month_name' ]

    ## Error checking
    
    queryStringParameters = validate_queryStringParameters(event)
    # filename and project are required
    if queryStringParameters == '':
        return {
        'statusCode': 401,
        'body': 'filename and project_id query parameters are required'
        }

    looker_header_token = check_headers(event)
    # looker header must be present
    if looker_header_token == '':
        return {
        'statusCode': 401,
        'body': 'invalid payload headers'
        }

    if 'project_config' in os.environ:
        config = json.loads(os.environ['project_config'])
    else:
        return {
        'statusCode': 401,
        'body': 'project_config is missing'
        }

    if looker_header_token in config:
        instance = config[looker_header_token]
    else:
        return {
        'statusCode': 401,
        'body': 'invalid project_config (instance webhook signature)'
        }

    if not ({'base_url','github_token','projects'} <= instance.keys() ):
        return {
        'statusCode': 401,
        'body': 'instance missing variables (base_url, github_token, projects)'
        }

    if not (type(instance['projects']) is list and len(instance['projects']) > 0 ):
        return {
        'statusCode': 401,
        'body': 'project is not list or length is 0'
        }
    
    body = check_body(event)
    ## body must be present
    if body == '':
        return {
            'statusCode': 401,
            'body': 'body missing from event'
        }

    # check for the fields key
    if 'scheduled_plan' in body and 'query' in body['scheduled_plan'] and 'fields' in body['scheduled_plan']['query']:
        fields = body['scheduled_plan']['query']['fields']
    else:
        return {
            'statusCode': 401,
            'body': 'selection not correct, check fields'
        } 

    # check fo rthe necessary fields
    required_fields = {'schema_table_search.table_schema', 'schema_table_search.table_name', 'schema_table_search.column_name', 'schema_table_search.type_convert', 'schema_table_search.comment'}
    if not (required_fields <= set(fields)):
        return {
            'statusCode': 401,
            'body': 'selection not correct, missing a required field'
        } 

    # check for body.attachment.data
    if 'attachment' in body and 'data' in body['attachment']:
        data = json.loads(body['attachment']['data'])
        # check that data has value
        if not check_data(data):
            return {
                'statusCode': 401,
                'body': 'No Attachment Data'
            } 
    else:
        return {
            'statusCode': 401,
            'body': 'No Attachment Data'
        } 

    # work with lookml
    
    fName = queryStringParameters['filename']+'.view.lkml'
    vw = View(queryStringParameters['filename'])
    
    vw.setSqlTableName(sql_table_name=str(data[0]['schema_table_search.table_name']),schema=str(data[0]['schema_table_search.table_schema']))

    for row in data:
        column = str(row['schema_table_search.column_name'])
        if str(row['schema_table_search.type_convert']) == 'time':
            dim = DimensionGroup(dbColumn=column)
        else:
            dim = Dimension(dbColumn=column)
            dim.setType(str(row['schema_table_search.type_convert']))  

        if row['schema_table_search.comment'] is not None:
            dim.setProperty('description', str(row['schema_table_search.comment']))    
        vw + dim

    ## GitHub API Section

    print(" begin github ")

    ## find project in config
    matched_project = {}
    print(fName)

    for project in instance['projects']:
        if queryStringParameters['project_id'] == project['project_id']:
            matched_project = project
    
    if not ( {'repository', 'project_id'} <= matched_project.keys() ):
        return {
            'statusCode': 401,
            'body': 'missing keys from project (X-Looker-Deploy-Secret, repository, project_id)'
        } 

    git = Github(instance['github_token'])

    # get github org
    repo = git.get_repo(matched_project['repository'])
    contents = repo.get_contents("")
    matched_content = None

    for content in contents:
        if content.path == fName:
            matched_content = content

    if matched_content is not None:
        repo.update_file(matched_content.path, "auto-update", str(vw), sha=matched_content.sha, branch="master")
    else:
        repo.create_file(fName, "new file", str(vw), branch="master")

    # hit deploy webhook

    if matched_project['X-Looker-Deploy-Secret'] is None or matched_project['X-Looker-Deploy-Secret'] == '':
        headers = {}
    else:
        headers={"X-Looker-Deploy-Secret": matched_project['X-Looker-Deploy-Secret']}

    r = requests.get(
        instance['base_url']+'/webhooks/projects/'+matched_project['project_id']+'/deploy',
        headers=headers)

    return {
        'statusCode': 200,
        'body': json.dumps('Deployed: '+instance['base_url']+'/projects/'+matched_project['project_id']+ '/files/' + fName)
    }


def check_headers(event):
    if 'headers' in event and 'X-Looker-Webhook-Token' in event['headers']:
        return event['headers']['X-Looker-Webhook-Token']
    else: 
        return ''
    
def check_body(event):
    if 'body' in event:
        return json.loads(event['body'])
    else:
        return ''

def check_fields(body):
    return True

def check_data(data):
    if data is None:
        return False
    elif len(data) > 0:
        return True
    else:
        return False

def validate_queryStringParameters(event):
    # filename and project_id are required
    if 'queryStringParameters' in event:
        if {'filename', 'project_id'} <= event['queryStringParameters'].keys():
            return event['queryStringParameters']
        else:
            return ''
    else:
        return ''
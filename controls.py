import boto3
import pandas as pd 
import sys
    
# if you want to search an specific framework, please include in the lista as string
# ej frameworks = ['c9bed0e0-ac88-35c7-bc64-61ea073dce0c']

frameworks = ['']

if not frameworks:
    response = clientAM.list_assessment_frameworks(
        frameworkType='Standard'
    )
    for i in response['frameworkMetadataList']:
        frameworks.append(i['id'])
if not sys.argv[1]:
    fileName = "file.csv"
else:
    fileName = sys.arg[1]

GetControls(fileName, frameworks)
    
def GetControls(fileName, frameworks):
    
    clientAM = boto3.client('auditmanager')
    
    f_ids = []
    f_arns = []
    f_names = []
    f_complianceType = []
    f_totalControls = []
    c_id = []
    c_name = []
    c_description = []
    c_controlSources = []
    
    for i in frameworks:
        
        response = clientAM.get_assessment_framework(
            frameworkId=i
        )
        controlsets = response['framework']['controlSets']
        for j in controlsets:
                controls = j['controls']
                for c in controls:
                    #f_ids.append(response['framework']['id'])
                    #f_arns.append(response['framework']['arn'])
                    f_names.append(response['framework']['name'])
                    f_complianceType.append(response['framework']['complianceType'])
                    #c_arnappend(c['arn'])
                    c_id.append(c['id'])
                    c_name.append(c['name'])
                    if "description" in c:
                        c_description.append(c['description'])
                    else:
                        c_description.append("")
                    c_controlSources.append(c['controlSources'])
                
    dict={'FrameworkName': f_names,'ComplianceType': f_complianceType, 'ControlId': c_id,
        'ControlName': c_name, 'ControlDescription': c_description, 'Sources':c_controlSources }
    df = pd.DataFrame(dict) 
    df.to_csv(fileName, sep=';') 

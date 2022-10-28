import re
from urllib import response
from botocore.exceptions import ClientError
from datetime import date, datetime
import boto3
import json
   



region = 'eu-west-1'
'''
s3 = botto_session.resource('s3')
s3 = botto_session.resource('s3')

sns_client=botto_session.client('sns')
ec2Client=botto_session.client('ec2')
availabilityZone = ec2Client.describe_availability_zones()'''
#lambdaClient = botto_session.client('lambda')
#Helper Method
def json_datetime_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

# print(s3.get_bucket_policy(Bucket="test-bucket-udubs"))

# print(ec2Client.describe_instances()["Reservations"][0]['Instances'])
# print(ec2Client.describe_instances())

# ec2button=[]
# bucket=[]
# #ui="ec2"
# client = botto_session.client('config')
# #nstances=client.describe_instances()

# response = client.list_discovered_resources(resourceType="")
# print(response)


# client = botto_session.client('config')

# resources = ["AWS::EC2::Host"]
# for resource in resources:
#     response = client.list_discovered_resources(resourceType=resource)
#     print(response)

def get_ec2(botto_session):
    returnArr=[]
    print("Session")
    print(botto_session)


    ec2_resource=botto_session.resource('ec2')
    client=botto_session.client('ec2')
    instances=client.describe_instances()["Reservations"]
   # print(json.dumps(instances[0]["Instances"][0],indent=4,default=json_datetime_serializer))
    for instance in instances:
        ebsDict={"DeviceName":"","Ebs":{"VolumeType" : "",
                            "Iops" : "",
                            "DeleteOnTermination" : "",
                            "VolumeSize" : ""}}

        ec2Dict={"Type":"AWS::EC2::Instance",
            "Properties":{
                "ImageId" :"",
                "InstanceType":"",
                "KeyName":"",
                "BlockDeviceMappings" : [
                    ebsDict
                    , 
                    {
                        "DeviceName" : "/dev/sdk",
                        "NoDevice" : {}
                    }
                ],
                "Tags":""
            }
    }
        for intop,itemtop in enumerate(instance["Instances"]):
            for key in instance["Instances"][intop]:
                if key == "Tags":
                    ec2Dict["Properties"]["Tags"]=instance["Instances"][intop][key]
                    #print(instance["Instances"][0][key])
                    #print()
                elif key == "BlockDeviceMappings":
                    #print(instance["Instances"][intop][key])
                    for index, item in enumerate(instance["Instances"][intop][key]):
                        if "Ebs" in list(item.keys()):
                            #print(ec2_resource.volumes.filter(VolumeIds=instance["Instances"][0][key][index]["Ebs"]["VolumeId"]).volume)
                            #print(ec2_resource.Volume(instance["Instances"][0][key][index]["Ebs"]["VolumeId"]))
                            #print(instance["Instances"][0][key][index]["Ebs"]['DeleteOnTermination'])
                            ebsDict['Ebs']['DeleteOnTermination']=instance["Instances"][intop][key][index]["Ebs"]['DeleteOnTermination']
                            ebsDict['Ebs']['VolumeType']=ec2_resource.Volume(instance["Instances"][intop][key][index]["Ebs"]["VolumeId"]).volume_type
                            ebsDict['Ebs']['VolumeSize']=ec2_resource.Volume(instance["Instances"][intop][key][index]["Ebs"]["VolumeId"]).size
                            try:
                                if ec2_resource.Volume(instance["Instances"][intop][key][index]["Ebs"]["VolumeId"]).volume_type not in ["io1","io2","gp3"]:
                                    ebsDict['Ebs'].pop("Iops")
                                else:
                                    ebsDict['Ebs']['Iops']=ec2_resource.Volume(instance["Instances"][intop][key][index]["Ebs"]["VolumeId"]).iops
                            except KeyError:
                                print()
                elif key == "RootDeviceName":
                    ebsDict['DeviceName']=instance["Instances"][intop][key]
                elif key == "ImageId":
                    ec2Dict["Properties"]['ImageId']=instance["Instances"][intop][key]
                elif key =="KeyName":
                    ec2Dict["Properties"]['KeyName']=instance["Instances"][intop][key]
                elif key == "InstanceType":
                    ec2Dict["Properties"]['InstanceType']=instance["Instances"][intop][key]
        
        #returnArr.append(json.dumps(ec2Dict,indent=4,default=json_datetime_serializer))
        returnArr.append(ec2Dict)
        #for i in returnArr:
        #  print(i)
        #  print("###############")
    #print(returnArr)
    return returnArr


                #print(ec2_resource.volumes.filter(VolumeIds=["Instances"][0][key][0]["Ebs"]))
        #print(json.dumps(instance["Instances"][0],indent=4,default=json_datetime_serializer))
        #print(r"\n ################ new instance ############## \n")

def create_EC2(botto_session):
    client=botto_session.resource('ec2')
    instances = client.create_instances(
        ImageId="ami-09e2d756e7d78558d",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="test"
    )

# def CF_ec2(ImageID):
#     output={f"Type":"AWS::EC2::Instance",
#             "Properties":{
#                 "ImageId" :{ImageID},
#                 "KeyName":"test"},
#                 "BlockDeviceMappings" : [
#                     {
#                         "DeviceName" : "/dev/sdm",
#                         "Ebs" : {
#                             "VolumeType" : "io1",
#                             "Iops" : "200",
#                             "DeleteOnTermination" : "false",
#                             "VolumeSize" : "20"
#                                 }
#                     }, 
#                     {
#                         "DeviceName" : "/dev/sdk",
#                         "NoDevice" : {}
#                     }
#                 ]
#             }

#get_ec2()


def getBuckets(botto_session):
    s3 = botto_session.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket)
        print()



bucket_name = 'test-bucket-udubs'
bucket_policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Sid': 'AddPerm',
        'Effect': 'Allow',
        'Principal': '*',
        'Action': ['s3:GetObject'],
        'Resource': f'arn:aws:s3:::{bucket_name}/*'
    }]
}

def CF_bucket(botto_session):
    returnArr=[]

    client=botto_session.client("s3")
    s3=botto_session.resource('s3')
    for name in s3.buckets.all():
        returnJson={
    "Resources": {
        "S3Bucket": {
            "Type": "AWS::S3::Bucket",
            "Properties": {
                "BucketName": ""
            }
        }
    }
}
        try:
            returnJson["Resources"]["S3Bucket"]["Properties"]["BucketName"]="copy-of-"+name.name
            bucketTags = client.get_bucket_tagging(Bucket=name.name)['TagSet']
            returnJson["Resources"]["S3Bucket"]["Properties"]["Tags"]=bucketTags
            #returnArr.append(json.dumps(returnJson, indent=4))
            returnArr.append(returnJson)
        except:
            print(f" no tags for bucket {name.name}"),
            #returnArr.append(json.dumps(returnJson, indent=4))
            returnArr.append(returnJson)
        #print(json.dumps(returnJson, indent=4))

    return returnArr

def add_policy(name,policy):

    bucket_policy = json.dumps(policy)
    #print(bucket_policy)
    s3 = botto_session.client('s3')

    s3.put_bucket_policy(Bucket=name, Policy=bucket_policy)
    return print(f"policy added: {policy}")

def remove_policy(name):
    s3 = botto_session.client('s3')
    s3.delete_bucket_policy(Bucket=name)
    return print('policy')
def getPolicy(name):
    s3 = botto_session.client('s3')
    result = s3.get_bucket_policy(Bucket=name)
    return print(f"policy for bucket > {name}:{result['Policy']}")

def createBucket(name,location):
    s3_client = botto_session.client('s3')
    #location = {'LocationConstraint': region}
    s3_client.create_bucket(Bucket=name,
                        CreateBucketConfiguration={'LocationConstraint':location})

#add_policy(bucket_name, bucket_policy)
#createBucket("simple-bucket-udubs",'eu-west-1')
#getBuckets()
#getPolicy(bucket_name)


#START of VPC functionscls

#Describe VPCs
def describe_vpcs(botto_session):
    """
    Describes one or more of your VPCs.
    """
    vpc_client = botto_session.client("ec2")
    try:
        # creating paginator object for describe_vpcs() method
        paginator = vpc_client.get_paginator('describe_vpcs')

        # creating a PageIterator from the paginator
        response_iterator = paginator.paginate()
        full_result = response_iterator.build_full_result()

        vpc_list = []

        for page in full_result['Vpcs']:
            vpc_list.append(page)

    except ClientError:
        print('Could not describe VPCs.')
        raise
    else:
        return vpc_list

def get_vpc(botto_session):
    
    vpcs = describe_vpcs(botto_session)
    returnArr=[] 
    for vpc in vpcs:
        #print(vpc)        
        #output=''
        #output=output+('"MyVPC" :{'+'\n')
        #output=output+('   "Type" : "AWS::EC2::VPC",'+'\n')
        #output=output+('   "Properties" :'+json.dumps(vpc, indent=8) + '\n'+'}'+'\n')
        output={"MyVPC":{"Type":"","Properties":""}}
        output["MyVPC"]["Type"]="AWS::EC2::VPC"
        output["MyVPC"]["Properties"]=vpc
        #print(output)
        returnArr.append(output)
    return returnArr    

def vpcButtons():
    returnDict={}
    for vpc in get_vpc():               
        returnDict[vpc["MyVPC"]['Properties']["Tags"][0]["Value"]]=json.dumps(vpc,indent=4,default=json_datetime_serializer)                    
    return returnDict

#Describe VPC Attribute
def describe_vpc_attribute(vpc_id, attribute):
    """
    Describes the specified attribute of the specified VPC.
    """
    try:
        response = vpc_client.describe_vpc_attribute(Attribute=attribute,VpcId=vpc_id)
    except ClientError:
        print('Could not describe a vpc attribute.')
        raise
    else:
        return response
  # Constantscls


def output_vpc(vpc_cdir,key,value):
 output={"MyVPC" : {"Type" : "AWS::EC2::VPC","Properties" : { "CidrBlock" : vpc_cdir,"Tags" : [ {"Key" : key, "Value" : value}]}}}
 return output

#END of VPC funcitons

#>>>>START of VPC Calls
# TAG = 'Name'
# TAG_VALUES = ['myVPC']
# MAX_ITEMS = 10


# VPC_ID = 'vpc-0b521fce0cd703801'
# #Another ATTRIBUTE would be 'enableDnsHostnames'
# ATTRIBUTE = 'enableDnsSupport'    
# custom_vpc_attribute = describe_vpc_attribute(VPC_ID, ATTRIBUTE)
# print(f'VPC attribute details: \n{json.dumps(custom_vpc_attribute, indent=4)}') 
#>>>>END of VPC Calls


#START of EBS functions
 describe_response = ec2Client.describe_volumes(
     VolumeIds=[
         'vol-05f3155ee9390010b'
     ]
 )

def ebsButtons():
    returnDict={}
    for ebs in get_EBS():            
        returnDict[ebs["Volumes"][0]["Tags"][0]["Value"]]=json.dumps(ebs,indent=4,default=json_datetime_serializer)                    
    return returnDict

def get_EBS(botto_session):
    ec2Client=botto_session.client('ec2')
    returnArr=[]
    for attachment in ec2Client.describe_volumes()['Volumes']:
        describe_response = ec2Client.describe_volumes(VolumeIds=[attachment['VolumeId']])
        describe_response.pop('ResponseMetadata')
        returnArr.append(describe_response)
    return returnArr
    # for attachment in ec2Client.describe_volumes()['Volumes']:
    #     describe_response = ec2Client.describe_volumes(VolumeIds=[attachment['VolumeId']])
    #     print(json.dumps(describe_response,indent=4,default=json_datetime_serializer)+'\n')
    #     for volume in attachment['Attachments']:
    #        #print(attachment['Attachments'][0]['VolumeId'])
    #         #print(volume['VolumeId'])
    #         describe_response = ec2Client.describe_volumes(VolumeIds=[volume['VolumeId']])
    #         print(json.dumps(describe_response,indent=4,default=json_datetime_serializer))
            

def output_ebs(size,key,value,):
    output={"NewVolume" : {"Type" : "AWS::EC2::Volume","Properties" : {"Size" : size,"Encrypted" : "true","AvailabilityZone" : "eu-west-1b","Tags" : [ {"Key" : key, "Value" : value} ]},"DeletionPolicy" : "Snapshot"}}
    return output

#END of EBS functions

#>>>>START of EBS Calls

#)

#>>>>END of EBS Calls

#START of SNS functions

def list_topics(sns_client):
    """
    Lists all SNS notification topics using paginator.
    """
    try:

        paginator = sns_client.get_paginator('list_topics')

        # creating a PageIterator from the paginator
        page_iterator = paginator.paginate().build_full_result()

        topics_list = []

        # loop through each page from page_iterator
        for page in page_iterator['Topics']:
            topics_list.append(page['TopicArn'])
    except ClientError:
        logger.exception(f'Could not list SNS topics.')
        raise
    else:
        return topics_list

def snsButtons():
    returnDict={}
    for sns in get_sns():               
        returnDict[sns["MySNSTopic"]['Properties']["TopicArn"]]=json.dumps(sns,indent=4,default=json_datetime_serializer)                  
    return returnDict

def get_sns(botto_session):

    sns_client=botto_session.client('sns')
    topics = list_topics(sns_client)
    returnArr=[]
    print(topics)
    print("-----------")
    for sns in topics:
        topic_name=sns.split(":")[-1]
        output={"MySNSTopic":{"Type":"","Properties":{"Endpoint":"","Protocol":"","TopicArn":""}}}
        output["MySNSTopic"]["Type"]="AWS::SNS::Subscription"
        output["MySNSTopic"]["Properties"]["Endpoint"]="e-flash@oldmutual.com"
        output["MySNSTopic"]["Properties"]["Protocol"]="email"
        output["MySNSTopic"]["Properties"]["TopicArn"]=sns
        output["topic_name"]=topic_name
        returnArr.append(output)
    return returnArr  

def output_snsTopicSubscription(protocol,endpoint,topic):
    output={"MySNSTopic" : {"Type" : "AWS::SNS::Topic","Properties" : {"Subscription" : [{"Endpoint" : endpoint,"Protocol" : protocol} ], "TopicName" : topic} }}
    return output

def output_snsTopicOnly(protocol,endpoint,topic):
    output={"MySNSTopic" : {"Type" : "AWS::SNS::Topic","Properties" :{  "TopicName" : topic }}}
    return output

#>>>>END of SNS functions

#START of Lambda Call
# response = lambdaClient.get_function(FunctionName='NameOfLambdaCall')
# response = lambdaClient.list_aliases(
#     FunctionName='helloWorldLambda',
#     FunctionVersion='1',
# )

# aliases = response['Aliases']
# print(response)
#END of Lambda Call



# Functions for formatting the FrontEnd

def bucketButtons():
    returnDict={}
    for bucket in CF_bucket():
        returnDict[bucket["Resources"]['S3Bucket']['Properties']['BucketName']]=json.dumps(bucket, indent=4)
    return returnDict

def ec2buttons(botto_session):
    returnDict={}
    arr=[]
    for instance in get_ec2(botto_session):
        for index,tags in enumerate(instance['Properties']["Tags"]):
            if tags["Key"] == "Name":
                pos=index
                #print(arr)
                #print("hello" +  tags["Value"])
                
                if tags["Value"] in arr:
                    returnDict[instance['Properties']["Tags"][pos]["Value"]+str(pos)]=json.dumps(instance,indent=4,default=json_datetime_serializer)
                else:
                    returnDict[instance['Properties']["Tags"][pos]["Value"]]=json.dumps(instance,indent=4,default=json_datetime_serializer)
                arr.append(tags["Value"])
    return returnDict


def create_rds_mysql(botto_session):
    arr =[]
    Conn=botto_session.client('rds')
    #pDbName=input("enter DBname") 
    #pDbUser=input("user name") 
    #pDbPass= input("enter password")

    client = botto_session.client('rds')
    
    response = client.describe_db_instances()
    
    #print("response")
    #print(response)
    #print("--------------------------")
    
    for i in response['DBInstances']:
        #pDbName=input("enter DBname") 
        #pDbUser=input("user name") 
        #pDbPass= input("enter password")
        db_instance_name = i['DBInstanceIdentifier']
        db_type = i['DBInstanceClass']
        db_storage = i['AllocatedStorage']
        db_engine = i['Engine']
        db_storage_type=i['StorageType']
        db_AvailabilityZone= i['AvailabilityZone']
        pDbUser=i['MasterUsername']
        #print (db_instance_name,db_type,db_storage,db_engine,db_AvailabilityZone,db_storage_type)

        Last_met= {
                    "db_name":db_instance_name,
        
                    "template":{"Type":"AWS::RDS::DBInstance",
                        "Properties":{
                            "DBName":"test1",
                            "MasterUsername":pDbUser,
                            "MasterUserPassword" : "Duwain123",
                            "Engine":db_engine,
                            "DBInstanceClass":db_type,
                            "StorageType":db_storage_type,
                            "PubliclyAccessible":"False",
                            "AllocatedStorage":db_storage,
                            "AvailabilityZone":db_AvailabilityZone
                        }

                    }
                    }
        
        arr.append(Last_met)
    return arr

def rds_button(botto_session,):
    returnDict={}
    arr_2=[]

    for dbinstance in create_rds_mysql(botto_session):
        for index,engine in enumerate(dbinstance['Properties']["Engine"]):
            #dbinstance['Properties']["MasterUsername"]=username
            #dbinstance['Properties']["MasterUserPassword"]= password
            #dbinstance['Properties']["DBName"] =dbname
            returnDict[dbinstance['Properties']["Engine"]]=json.dumps(dbinstance,indent=4,default=json_datetime_serializer)
            arr_2.append(engine)
    print(returnDict)
    return returnDict
   
   
#################################
#>>>>>>> Call Functions Below <<<<<<<<<<<

#get_ec2()
#create_EC2()
#CF_bucket()
#get_EBS()
#get_sns()
#[print(json.dumps(k,indent=4,default=json_datetime_serializer)) for k in get_vpc()]
#vpcButtons()
#ebsButtons()
#get_sns()
#snsButtons()
#[print(k) for k in ec2buttons()]
#print(bucketButtons())


#print(json.dumps(output_vpc('10.0.0.0/16','Name','myVPC'),indent=4))
#print(output_ebs('100','Name','Test-ebs'))





##################################

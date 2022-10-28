import tkinter as tk
import FunctionsForConfigs as ffc
import boto3
import tkinter.messagebox
import os
import json
from tkinter import *
import re


awsSession = boto3.session.Session()
profile_name="default"
datalist={}
frameArray=[]
itemCount=0
checkboxArray=[]
templateDict={}

def GUI():
    window=tk.Tk()
    
    window.title("Resources to CloudFormation Generator")
    window.geometry("600x450")
    
    sessionLabel = tk.Label(window, text="AWS Profile", highlightthickness = 14)
    sessionLabel.grid(row=0, column=0)
    #sessionLabel.pack()
    sessionEntry = tk.Entry(window)
    sessionEntry.grid(row=0, column=1)
    
    buttonSession = tk.Button(window, text="SetSession", command=lambda: setSession(sessionEntry) )
    buttonSession.grid(row=0, column=2)
    
    dividerLabel = tk.Label(window, text="         ", highlightthickness = 14)
    dividerLabel.grid(row=1, column=0, columnspan=6)
    
    
    
    ResourcesFrame= tk.Frame(window, width=500)
    ResourcesFrame.grid( row=3, column=0, columnspan=6)
    canvas = tk.Canvas(ResourcesFrame, width=500)
    
    scrollbar = tk.Scrollbar(ResourcesFrame, orient="vertical", command=canvas.yview)
    
    
    
    
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar.pack(side="right", fill=Y)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    
    
    canvasFrame=tk.Frame(canvas)
    canvas.create_window((0,0),window=canvasFrame, anchor="nw")
    canvasFrame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    buttonResources = tk.Button(window, text="ShowResources", command=lambda: packResources(canvasFrame) )
    buttonResources.grid(row=2,column=0)
    
    buttonTemplate = tk.Button(window, text="Generate Template", command=lambda: getTemplate() )
    buttonTemplate.grid(row=5, column=0, columnspan=2)
    
    
    
    
    
    
    window.mainloop()
    
def setSession(sessionEntry):

    global profile_name
    profile_name= sessionEntry.get()
    
    
    try:
        global awsSession
        awsSession=boto3.session.Session(profile_name=profile_name)
        
        tkinter.messagebox.showinfo(title="Sucess", message="AWS profile set sucessfully")
        #success
    
    except:
        print("error")
        tkinter.messagebox.showerror(title="Error", message="Failed to set AWS profile")
    printTest()
    

def packResources(canvasFrame):
    
    typeLabel = tk.Label(canvasFrame, text="Resource Type", highlightthickness = 14)
    
    typeLabel.grid(row=0, column=0)
    
    nameLabel = tk.Label(canvasFrame, text="Resource Name", highlightthickness = 14)
    nameLabel.grid(row=0, column=1)
    
    addLabel = tk.Label(canvasFrame, text="Add Resource", highlightthickness = 14)
    addLabel.grid(row=0, column=2)
    
    rowCount=1


    
    #add table
    
    
    global profile_name,awsSession
    print(profile_name)
    os.environ['AWS_PROFILE'] = profile_name
    
    #ec2Data=ffc.get_ec2(awsSession)
    
    global datalist
    global frameArray
    global itemCount
    itemCount=0
    
    
    ec2Data=ffc.ec2buttons(awsSession)
    
    for data in ec2Data:
    
        
        
        frameArray.append(tk.Label(canvasFrame, text=json.loads(ec2Data[data])["Type"], highlightthickness = 14))
        frameArray[-1].grid(row=rowCount, column=0)
    
        frameArray.append(tk.Label(canvasFrame, text=data, highlightthickness = 14))
        frameArray[-1].grid(row=rowCount, column=1)
        
        data_name = data.replace(" ", "").replace("-", "") 
        checkboxArray.append([IntVar(),data_name,json.loads(ec2Data[data])])
        frameArray.append(tk.Checkbutton(canvasFrame, text="add", variable=checkboxArray[itemCount][0]))
        frameArray[-1].grid(row=rowCount, column=2)
        
        rowCount=rowCount+1
        itemCount=itemCount+1
        
        
    '''
        
    s3Data=ffc.CF_bucket(awsSession)
    #print(json.dumps(s3Data))
    
    for data in s3Data:
    
        
        
        frameArray.append(tk.Label(canvasFrame, text=data["Resources"]["S3Bucket"]["Type"], highlightthickness = 14))
        frameArray[-1].grid(row=rowCount, column=0)
    
        frameArray.append(tk.Label(canvasFrame, text=data["Resources"]["S3Bucket"]["Properties"]["BucketName"], highlightthickness = 14))
        frameArray[-1].grid(row=rowCount, column=1)
        
        data_name = data["Resources"]["S3Bucket"]["Properties"]["BucketName"].replace(" ", "").replace("-", "") 
        checkboxArray.append([IntVar(),data_name,data["Resources"]["S3Bucket"]])
        frameArray.append(tk.Checkbutton(canvasFrame, text="add", variable=checkboxArray[itemCount][0]))
        frameArray[-1].grid(row=rowCount, column=2)
        
        rowCount=rowCount+1
        itemCount=itemCount+1
    '''
    
    rdsData=ffc.create_rds_mysql(awsSession)
    
    for data in rdsData:
    
        
        
        frameArray.append(tk.Label(canvasFrame, text=data["template"]["Type"], highlightthickness = 14))
        frameArray[-1].grid(row=rowCount, column=0)
    
        frameArray.append(tk.Label(canvasFrame, text=data["db_name"], highlightthickness = 14))
        frameArray[-1].grid(row=rowCount, column=1)
        
        data_name = data["db_name"].replace(" ", "").replace("-", "") 
        checkboxArray.append([IntVar(),data_name,data])
        frameArray.append(tk.Checkbutton(canvasFrame, text="add", variable=checkboxArray[itemCount][0]))
        frameArray[-1].grid(row=rowCount, column=2)
        
        rowCount=rowCount+1
        itemCount=itemCount+1
        
        
        
    snsData=ffc.get_sns(awsSession)
    
    for data in snsData:
    
        
        
        frameArray.append(tk.Label(canvasFrame, text=data["MySNSTopic"]["Type"], highlightthickness = 14))
        frameArray[-1].grid(row=rowCount, column=0)
    
        frameArray.append(tk.Label(canvasFrame, text=data["topic_name"], highlightthickness = 14))
        frameArray[-1].grid(row=rowCount, column=1)
        
        data_name = data["topic_name"].replace(" ", "").replace("-", "").replace(".", "")
        checkboxArray.append([IntVar(),data_name,data["MySNSTopic"]])
        frameArray.append(tk.Checkbutton(canvasFrame, text="add", variable=checkboxArray[itemCount][0]))
        frameArray[-1].grid(row=rowCount, column=2)
        
        rowCount=rowCount+1
        itemCount=itemCount+1
        
        '''
    
    s3Data=ffc.getBuckets(awsSession)
    
    
    
    rdsData=ffc.create_rds_mysql(awsSession)
    vpcData=ffc.get_vpc(awsSession)
    ebsData=ffc.get_EBS(awsSession)
    snsData=ffc.get_sns(awsSession)
    '''
    
    
    
    print("done")
    
def getTemplate():
    global templateDict
    
    templateDict={
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {
        
        }
    
    }
    global checkboxArray
    #print(checkboxArray)
    
    for resource in checkboxArray:
        if resource[0].get()==1:
            templateDict["Resources"][resource[1]]=resource[2]
    print(templateDict)
    
    with open("GeneratedTemplate.json", "w") as outfile:
        json.dump(templateDict, outfile)
    
    
    




def printTest():
    print(awsSession)
GUI()
    



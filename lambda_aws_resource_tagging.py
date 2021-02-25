import boto3

def lambda_handler(event, context):
    
    resource_arns = []
    total_results = []
    
    client = boto3.client('resourcegroupstaggingapi')
    
    # Get all resources. Note:- Only gets resources that are currently tagged or ever had a tag. 
    def get_resources(token):
        response = client.get_resources(
            PaginationToken=token,
            ResourcesPerPage=50,
        )
        return response
      
    def tag_resources(resource_arns):
        tag_response = client.tag_resources(
            ResourceARNList= resource_arns,
            Tags={
                'Environment': 'Development'
            }
        )
        return tag_response
        
    
    response = get_resources("")
    page_token = ""
    while True:
        total_results += response["ResourceTagMappingList"]
        page_token = response["PaginationToken"]
        if page_token == "":
            break
        response = get_resources(page_token)
    for result in total_results:
        resource_arns.append(result["ResourceARN"])
    
    # Tag all resources
    try:
        tag_response = tag_resources(resource_arns)
        print("Below resources have been tagged:\n")
        print("\n".join(resource_arns))

    except:
        print("An exception occurred")
    
    

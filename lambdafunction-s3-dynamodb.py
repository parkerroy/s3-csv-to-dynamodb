import boto3

s3_client = boto3.client("s3")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('teams')

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    s3_file_name = event['Records'][0]['s3']['object']['key']
    resp = s3_client.get_object(Bucket=bucket_name,Key=s3_file_name)
    data = resp['Body'].read().decode("utf-8")
    team = data.split("\n")
    for t in team:
        print(t)
        t_data = t.split(",")
        #Add it to dynamodb
        try:
            table.put_item(
            Item = {
                "id" : t_data[0],
                "location" : t_data[1],
                "teams" : t_data[2]
            }
            )
        except Exception as e:
            print("End of File")

import main

def lambda_handler(event, context):

    df = main()
    return df
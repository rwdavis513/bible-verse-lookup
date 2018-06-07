dir=`ls`
if [ ! $dir = *"app"* ]
then
   echo "app directory not found in " + $dir
   exit
fi

cp -r app /tmp
cd /tmp/app
pip install -r requirements.txt -t .
zip -R lambda_function.zip *
s3_location=s3://$S3_BUCKET/lex_bot_lambda.zip
if [ ! $S3_BUCKET ]
then
   echo "S3_BUCKET not found in environmental variables."
   exit
fi

echo "s3 location:" + $s3_location
aws s3 cp lambda_function.zip $s3_location

if [ $1 ]
then
if [ $1 = "--update" ]
then
   echo "Updating Lambda function"
   ##aws lambda create-function --function-name lex_bot_lambda --runtime python3.6 --role ? --handler lambda_handler --zip-file lambda_function.zip
   aws lambda update-function-code --function-name lex_bot_lambda --s3-bucket $S3_BUCKET --s3-key lex_bot_lambda.zip
fi
fi
echo "Complete"

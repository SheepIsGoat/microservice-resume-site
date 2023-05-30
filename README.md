# Personal Resume Microservice
Deploy your own personal resume site using AWS ECS and CloudFormation. This template contains a resume and 'ContactMe' functionality, but it's easily extensible for showing off personal projects. 

Please credit Dylan Funk funk.ml.engineering@gmail.com

TODO: Works on port 80 (http), needs port 443 (https)

## Docker

### Set up environment
First get your 12-digit AWS account id
```
export AWS_ACCOUNT_ID="<your_acct_id_here>"
```
Next, you can change the following variables in your docker-task.sh file
```
IMAGE_NAME="dylan_funk_personal_backend"  # rename this
CONTAINER_NAME="personal-site-flask"  # keep or change
AWS_REGION="us-east-2"  # change to your region
```
### Build
```
sh docker-task.sh build
```

### Test your local stack
```
$ docker compose up -d
```

After the application starts, navigate to http://localhost:8000 in your web browser

### Development
To make changes and test, you need to rebuild. An easy shortcut is
```
sh docker-task.sh buildrun
```


### Deploy with ECR Repository
```
sh docker-task.sh createrepo
```

You can then [open the ECR Console](https://console.aws.amazon.com/ecs/home#/repositories "ECR Console") to verify that is was created.

```
sh docker-task.sh buildpush
```

Print your image name to input in the text step, in the cloudformation console
```
sh docker-task.sh showimage
```

## Create your CloudFormation Stack in AWS
Go to [CloudFormation in the console](https://us-east-2.console.aws.amazon.com/cloudformation/home "ECS Console") and create a new stack.
1. Upload a template file (upload your cloudformation.yml)
2. View in designer
3. Verify
4. Go back to creating a stack (you may have to reupload the .yml)
5. Fill in the parameters


You should now have a cloudformation stack where you can go to all the AWS resources created for your personal website. [CloudFormation in the console.](https://us-east-2.console.aws.amazon.com/cloudformation/home "ECS Console") Here you can see all the resources you've created, check them if anything is wrong, or change them if you want to make small adjustments.


---
### <b>Troubleshooting</b> a hanging stack

1. Go to your cloudformation stack (or [ECS in the console](https://us-east-2.console.aws.amazon.com/ecs/v2/clusters "ECS Console"))
2. Click on your new cluster 'ECSCluster'
3. Click on your service
4. Check if it's healthy, if not then continue to step 5
5. Go to the Events tab
6. Look for an event that looks like this and click on the task `service personal-website-service-27xcoED2XlTV has started 1 tasks: task` <b>`cab113fbcc144bd78b22dc500cc4d915.`</b>
7. It should explain why the issue is happening
---

### Go to your live website
1. Go to [EC2 in the console](https://us-east-2.console.aws.amazon.com/ec2/home "EC2 Console")
2. Click on your ALBListener (also available from EC2>Load Balancers)
3. Click on the load balancer
4. Copy the DNS name - your site is now publicly available!

## Register DNS
In order to have your own custom domain name, if you don't already, you should register your DNS name. I used AWS Route 53 since it allows me to do everything within AWS, but there are better DNS providers out there.


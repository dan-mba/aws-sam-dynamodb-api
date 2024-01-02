# AWS SAM DynamoDB Skills API

An API to store skills & ratings for multiple users in a DynamoDB table.<br>
All routes are protected by Cognito & require the JWT in the Authorization header<br>
The username from the JWT is stored with each item in the table<br> 

## Parameter Definitions
rating: Integer (1-5) representing expertise level<br>
skill: String representing a specific skill<br>

## API Definition

GET /Skills - Get all skills<br>
GET /Skills/{rating} = Get skill with specified rating<br>

POST /Skills - Add skill
```js
body: {
  "rating": "rating Integer",
  "skill": "skill String"
}
```

PUT /Skills - Update skill rating
```js
body: {
  "oldrating": "current rating Integer",
  "newrating": "new rating Integer",
  "skill": "skill String"
}
```

DELETE /Skills/{rating}/{skill} - Delete selected skill

DELETE /Skills/ALL_SKILLS - Delete all skills



## AWS SAM Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)

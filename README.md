# AWS SAM DynamoDB Skills API

An API to store skills & ratings for multiple users in a DynamoDB table.<br>
The userid is a paramater in this simple implementation.<br>
In production it would be obtained from the authentication provider (Cognito).

## Parameter Definitions
userid: String representing a specific user<br>
rating: Integer (1-5) representing expertise level<br>
skill: String representing a specific skill<br>

## API Definition

GET /Skills/{userid} - Get all skills for specified userid<br>
GET /Skills/{userid}/{rating} = Get skill with sepcified rating for specifeid userid<br>

POST /Skills - Add skill
```json
body: {
  "userid": "userid String",
  "rating": "rating Integer",
  "skill": "skill String"
}
```

PUT /Skills - Update skill rating
```json
body: {
  "userid": "userid String",
  "oldrating": "current rating Integer",
  "newrating": "new rating Integer",
  "skill": "skill String"
}
```

DELETE /Skills - Delete selected skill
```json
body: {
  "userid": "userid String",
  "rating": "rating Integer",
  "skill": "skill String"
}
```

DELETE /Skills - Delete all skills for sepecifed userid
```json
body: {
  "userid": "userid String",
  "confirm": "YES"
}
```


## AWS SAM Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)

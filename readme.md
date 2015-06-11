# Flask RESTful Survey API

A flask implementation of a REST survey API. 

There are four main objects:

1. Questions - Can be used in multiple surveys
2. Answers - Responses to questions, associated with a survey response
3. Surveys - A parent to answers and responses
4. Responses - A response to a survey object

## To Do:

~~1. Validation of created/updated db objects~~

2. Add URI links for FK related objects in API output

3. Better exception and error handling

~~4. Have index show tables along with URI links~~

~~5. Make the survey list_q (question list) field be useful~~

6. Add security (prevent malicious input, user auth, etc)

7. Look into better ways to organize the code
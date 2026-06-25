# AWS Placement Eligibility Chatbot

## Overview

AWS Placement Eligibility Chatbot is a serverless chatbot built using Amazon Lex, AWS Lambda, and DynamoDB. It helps students quickly access placement-related information through a conversational interface.

## Features

* Company Information Lookup
* Eligibility Checking
* Company Comparison
* Technology Role Explanation
* Interactive Chatbot Interface

## AWS Services Used

* Amazon Lex
* AWS Lambda
* Amazon DynamoDB
* Amazon CloudWatch

## Architecture

Student → Amazon Lex → AWS Lambda → DynamoDB

## Implemented Intents

### WelcomeIntent

Greets the user.

### CompanyInfoIntent

Provides company details such as hiring scale and roles offered.

Example:

* Tell me about Amazon

### EligibilityIntent

Provides minimum CGPA requirements and eligible roles.

Example:

* Can I apply to Amazon?

### ComparisonIntent

Compares two companies based on hiring criteria.

Example:

* Compare Amazon vs Tesla

### RoleExplainerIntent

Explains different technology roles.

Examples:

* What is AI Engineer?
* Explain Backend Developer

### FallbackIntent

Handles unsupported queries gracefully.

## DynamoDB Schema

Table: Companies_tab

Attributes:

* CompanyName
* MinCGPA
* HiringScale
* TypicalRoles

## Technologies Used

* Python
* AWS Lex
* AWS Lambda
* DynamoDB
* CloudWatch

## Screenshots

Add screenshots of:

* Lex Bot
* Intents
* Lambda Function
* DynamoDB Table
* Chatbot Testing
* Architecture Diagram

## Future Improvements

* Add more companies
* Salary comparison feature
* Placement statistics
* Student profile-based recommendations
* Web interface integration

## Learning Outcomes

Through this project, I learned:

* AWS Lex chatbot development
* Serverless architecture
* DynamoDB integration
* Lambda function development
* Intent and slot management
* CloudWatch debugging

## Author

Aditya Sahu

Aspiring AI/ML and Cloud Engineer

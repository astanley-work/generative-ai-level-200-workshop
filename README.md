# Generative AI Level 200 Workshop

This session is focused on building with Generative AI on AWS.

In particular, it is focused on allowing people who advise customers on approaches to cost with Generative AI to get a hands on feel for how different approaches to pricing affect the customer and developer experiences.

The session is built around 3 tasks, each of which is built around a mock customer scenario.

## Scenario - Part 1:
As of today, you are an engineer working at Call Center Co (CCC)! (Call Center Support for a headset retailer)

With the launch of ChatGPT, your manager wants to get ahead of the curve and start adopting Generative AI ASAP.

Your colleague, ever eager, has already written the front-end for a Generative AI powered app. You just need to do the following 


## Task 1:
- Build a plan for experimenting with Generative AI models (estimate costs, decide which model to leverage for your PoC)
- Leverage your AWS account, as well as the code in the task-1 folder, to do implement the following architecture

![image](https://github.com/astanley-work/generative-ai-level-200-workshop/assets/77308012/5942a5ee-c891-41c3-b21e-c8f06b2b0b67)

Regarding DynamoDB, we recommend logging the following information

![image](https://github.com/astanley-work/generative-ai-level-200-workshop/assets/77308012/6027ca4c-a5d5-45f3-a791-a59b49ad9acb)

## Scenario - Part 2:
Congratulations! Now that you have a test application up, your teammates have started playing with it.

However, after reviewing your log data, you realize your initial cost estimates were too low (you now project 10,000 requests per day, with 5,000 input tokens and 1,000 output tokens).

To make the rollout more financially viable, your manager asks you to test out different, cheaper bedrock models.

## Task 2:
- Leveraging either the code and architecture setup you created in task 1 or a new architecture layout, re-create the chat experience of task 1 leveraging a different Bedrock model
- Evaluate your LLM's performance vs. your intial choice

## Scenario - Part 3:
Now that you have addressed issues of cost, your manager is interested in adding call center intelligence to your application.

To do this, we need to implement a version of Retrieval Augmented Generation (RAG).

## Task 3:
- Extend your task 1 and/or task 2 application to incorporate a RAG application, using Amazon OpenSearch as your vector store
- Use the amazon-pqa headsets dataset as your knowledge base

![image](https://github.com/astanley-work/generative-ai-level-200-workshop/assets/77308012/7bd3fe8e-54a6-4013-9878-32235d62b987)



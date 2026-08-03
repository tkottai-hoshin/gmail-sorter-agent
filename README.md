Purpose:

The real world enterprise use cases specifically for Agentic AI implementations is found in: IT Incident management, Customer Support Routing and Claims Processing. The Agent has to independently reason through all of the incidents, support tickets and claims. And, 
it MUST be running on a continuous basis, like auto pilot for Tesla's. Versus a RAG architecture that is running only when the end user submits a prompt. In an Agentic AI architecture, 
it is important that the 'script' or program you're running has properly defined this workflow for safe auto pilot execution - make sure all of the boundaries are properly defined (so that AI does not go out of control or make expensive mistakes!!). 

In this example, I built my own personal Gmail Sorting Agent. Basically, whenever I get a new email, and my script / program is running on autopilot, the Agent will sort my email based on the criteria that I have defined. It
will analyze the subject + body of text, and the agent will proceed to place that email in 3 different Label categories for me automatically - Reply Now, Reply later or No Action. 


Tech Stack:

- LangGraph
- Kimi K3
- Google API



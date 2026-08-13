Purpose:

The real world enterprise use cases, specifically for Agentic AI implementations, are commonly found in: 

- IT Incident management
- Customer Support Routing
- Claims Processing


In these scenarios, the Agent has to independently reason through all of the incidents, support tickets and claims. And, it MUST be running on a continuous basis, similar to Tesla's auto pilot functions. Versus a RAG architecture that is running only when the end user submits a prompt. 

Agentic AI:

For this example, the agent is sorting through a Gmail email address just to simulate a similar process where there is Inbound and Outbound requests that are happening - At A High Level.  Such is that, whenever I get a new email, and my script / program is running on autopilot, the Agent will sort my email based on the criteria that I have defined. The Agent analyzes the Subject + Body of Text, and the Agent will proceed to place that email in 3 different Label categories for me automatically 

                      1 Reply Now
                      2 Reply later 
                      3 No Action. 

Architecture: 

Some of the Tools that you have to define are for mainly analyzing the Subject + Body of Text. Depending on what type of email address this is, you can build tools to look for key words or phrases that make it a higher priority vs a lower priority. Any workflow that is automated to some extent and has a tool that is running this decision engine has to properly define the boundaries for this workflow for safe auto pilot execution - make sure all of the security, workflows and any 3rd party server communication elements properly defined in there are functioned to be called (search, code execution, APIs). 

Tooling: 

The two main tools are I've defined as python functions are: 1) Classify 2) Apply. 

In the first Node, the parameter for when the agent should classify the email as Reply Now, Reply Later, or No Action is in the Prompt Function itself → LLM decides the category. This is where changes can be made to this tool to be more granular - hard-coded rules, business logic, or workflow guardrails. 

Second node (apply_label) → Takes that category and actually puts the label on the email in Gmail

Fetch email → Classify email → Apply label → Done

LangGraph manages:

1 The state (email_id, subject, body, category, etc.)
2 The order of steps
3 Passing data from one step to the next

Feature -- What it means
Stateful- Remembers information between steps
Controllable - You decide the exact flow
Reliable - Better for production than free-form agents
Supports cycles - Can loop if needed
Human-in-the-loop - Can pause and ask a human for approval


Tech Stack:

- LangGraph
- Kimi K3 (Opensource LLM)
- GMail API



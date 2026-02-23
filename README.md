<h1 align="center">AI AGENT FOR SHOP</h1>
<p>This AI agent is designed to assist customers in the market by understanding natural language queries, searching for products, checking availability, placing orders and answering general questions.</p>

<h2>TECH STACK</h2>
<ul>
  <li>Python 3.13.2</li>
  <li>FastAPI (API endpoints)</li>
  <li>Pydantic (data validation)</li>
  <li>LangChain(agent logic)</li>
  <li>LangGraph(agent workflow)</li>
  <li>LLMs (intent classification, NER and outputs)</li>
  <li>Embedding model (text embeddings)</li>
  <li>Sequence to sequence model (translate the request into the language)</li>
</ul>

<h2>HOW IT WORKS</h2>
<p>The user sends a request. The agent determines the intent using LLM. The slots are extracted using the NER tool, then performs an action. The response is created and returned to the user. If necessary, the agent asks for confirmation.</p>

<h2>AGENT FUNCTIONALS:</h2>
<h3>INTENT CLASSIFICATION</h3>
<br>
<p>The project uses an <code>intents.json</code> file that contains all intents and their descriptions. This allows the model to understand in the prompt what each intent is responsible for. The file also includes slots that need to be filled by the NER models.</p>
<br>
EXAMPLE:
<br>
<img src="./.images/agent_workflow/intent_example.PNG" width="500">

<h4>INTENTS:</h4>
<br>
<ul>
<li>Find products.</li>
<li>Find similar.</li>
<li>Get order/s.</li>
<li>Make order/s.</li>
<li>Answer general question/s.</li>
<li>Did not classified(if model could not classify user query).</li>
</ul>
<p>File is located in src/intents.json</p>
<h3>TOOLS:</h3>
<ul>
<li>Find products in whole marketplace.</li>
<li>Find similar products on user query.</li>
<li>Get user orders(in future, we can bind on user account).</li>
<li>Make order/s with use articles of products.</li>
<li>Answer for general client questions.</li>
</ul>

<h2>THE GRAPHS LOOK LIKE THIS:</h2>
<h3>Main graph:</h3>
<br>
<img src="./.images/graphs/main_graph.png" alt="Main graph" width="600">

<h3>Subgraphs:</h3>

1) Subgraph for search operations:
    <img src="./.images/graphs/search_subgraph.png" width="400"><br><br>

2) Subgraph for insert operations:
    <img src="./.images/graphs/insert_subgraph.png" width="300"><br><br>

3) Subgraph for general operations:
    <img src="./.images/graphs/general_operations_subgraph.png" width="500">

<h2>EXAMPLE USAGE</h2>
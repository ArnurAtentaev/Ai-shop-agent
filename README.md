<h1 align="center">AI AGENT FOR SHOP</h1>

<h2 align="center">AGENT FUNCTIONALS:</h1>
1) <h2>INTENT CLASSIFICATION</h2>
<br>
<p>The project uses an intents.json file that contains all intents and their descriptions. This allows the model to understand in the prompt what each intent is responsible for. The file also includes slots that need to be filled by the NER models.</p>
<br>
- EXAMPLE:
<br>
<img src="./.images/agent_workflow/intent_example.PNG" width="400">

<h3>INTENTS:</h3>
<br>

- Find products.
- Find similar.
- Get order/s.
- Make order/s.
- Answer general question/s.
File is located in src/intents.json
<br>
<br>
2) <h2>TOOLS:</h2>
- Find products in whole marketplace.
- Find similar products on user query.
- Get user orders(in future, we can bind on user account).
- Make order/s with use articles of products.
- Answer for general client questions.

THE GRAPHS LOOK LIKE THIS:

<h3>**Main graph:**</h3>
<br>
<br>
<img src="./.images/graphs/main_graph.png" alt="Main graph" width="600">

<h2>Subgraphs:</h2>
1) Subgraph for search operations:
<br>
    <img src="./.images/graphs/search_subgraph.png" alt="Search subgraph" width="400"><br><br>

2) Subgraph for insert operations:
<br>
    <img src="./.images/graphs/insert_subgraph.png" alt="Insert subgraph" width="300"><br><br>

3) Subgraph for general operations:
<br>
    <img src="./.images/graphs/general_operations_subgraph.png" alt="General operations subgraph" width="500">
<br>
<br>

<h2>INTENTS:</h2>
<br>
- Find products.
- Find similar.
- Get order/s.
- Make order/s.
- Answer general question/s.
File is located in src/intents.json
<br>
<br>
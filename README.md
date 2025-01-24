#SITE MAP GENERATOR TOOL

##How to run
To run the virtual enviroment run:
  source .venv/bin/activate

Then run the following commands:
  export FLASK_DEBUG=1
  flask run

##Thoughts
- To make it faster could try updating the visual graph representation as the new pages are discovered. Can use either Server-Sent Events (SSE) or WebSockets to stream the updates.
- Can search until a cerain depth (e.g. 2) and only search further if the user clicks on the certain link (zooming in to the search).
 - In this case could also use user adaptive system or something like that to search links that are more commonly opened first.
- Could use distributed systems to make it faster.

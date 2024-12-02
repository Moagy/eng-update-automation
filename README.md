# eng-update-automation
This is a project to automate generation of weekly updates within my organisation. I manually create weekly updates by reading off our DevOps board and reaching out to my engineering and data science colleagues. Phase one of this project is to automate 'reading' of our board and output the JSON into a notepad.

06/11/2024
Discovered that WIQL query was only able to retrieve IDs from the URL method I was using. I am going to select certain IDs based on BoardColumn filters and state filters, group live updates, development updates and upcoming items IDs and then using for-loops extract details on each ID in each group and see where that leaves me.
Successfully got JSON object written into a file saved to my desktop. Phase 1 criteria half-met.
Added function to get the PAT from a file saved on my desktop for security.

02/12/2024
Added logging and error-handling throughout script after experimenting with functionality of WIQL and how best to solve the problem at hand. Utilised class and functions for optimisation and effeciency of code. Created a txt file and JSON object storing detail on the PBIs in question and refined SQL queries to extract relevant information for the time being.

Phase 1 (essential):
Create a tool to read the DevOps board and generate an output into a notepade file on my desktop.

Phase 2 (eventual): 
Automate the sending of requesting updates from individuals.

Phase 3 (nice-to-have):
Merge that individual feedback with the board updates, layered with a natural language toolkit to generate whitty but informative weekly updates for the wider organisation. 

import sys
sys.path.append('src/')
from biochatter_metta.prompts import BioCypherPromptEngine


prompt_engine = BioCypherPromptEngine(
                    model_name="gpt-3.5-turbo",
                    schema_config_or_info_path="./src/biochatter_metta/biocypher_config/schema_config.yaml",
                    schema_mappings='./src/biochatter_metta/biocypher_config/schema_mappings.json'
                )

""" Gene Ontology Atomspace queries: """
# user_question="What is the term name for the ontology term with ID 'GO:0000785'?"
# user_question="What is the regulatory region"
# user_question="Provide the description for the ontology term with ID 'GO:0000002'."
# user_question="What are the synonyms for the ontology term with ID 'GO:0002088'?"
# user_question="In which subontology does the ontology term with ID 'GO:0001654' belong?"
# user_question="What is the source URL for the ontology term with ID 'GO:0000015'?"
# user_question="What is the term name for the ontology term with ID 'GO:0000981'?"
# user_question="Give the description for the ontology term with ID 'GO:0000785'."
# user_question = "What is the subontology of the ontology term with ID 'GO:0000011'?"
# user_question = "Provide the term name and subontology for the ontology term with ID 'GO:0000785'." # ---
# user_question = "What is the subontology of the ontology term with ID 'GO:0000015'?"
# user_question = "Give me the term name and subontology for the ontology term with ID 'GO:0000028'."

# Questions from Metta-Motto
user_question = "What is gene ENSG00000237491 transcribed to?"
# user_question = "What are the transcripts of gene ENSG00000237491"
# user_question = "Get properties of gene ENSG00000279139"
# user_question = "Find pathways that gene F13A1 is a subset of"
# user_question = "Find parent pathways of the pathways that the gene named 'FGR' is a subset of?"
# user_question = "Find parent pathways of the pathways that FGR  gene is a subset of"

# user_question = "What variants have eqtl association with gene HBM"
# user_question = "What variants have eqtl association with gene ENSG00000206177"

response = prompt_engine.get_metta_response(user_question)
print(response)
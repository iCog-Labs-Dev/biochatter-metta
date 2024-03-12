import os
from hyperon import MeTTa
from biochatter.llm_connect import GptConversation
from biochatter.prompts import BioCypherPromptEngine


prompt_engine = BioCypherPromptEngine(
                    model_name="gpt-3.5-turbo",
                    schema_config_or_info_path="./biocypher_config/schema_config.yaml",
                )
# user_question="What is the name of the compound with id 'CID499989'?"
# user_question="What is the unit value for the descriptor with id 'Molecular_Weight'?"
# user_question = "What are the descriptor ids for the compound with id 'CID2499326'?"
# user_question="What is the Exact_Mass descriptor of the compound with id 'CID2499326'? In this case you can take 'Exact_Mass' as the descriptor id"

# user_question="What is the term name for the ontology term with ID 'GO:0000001'?"
# user_question="Provide the description for the ontology term with ID 'GO:0000002'."
# user_question="What are the synonyms for the ontology term with ID 'GO:0000005'?"
# user_question="In which subontology does the ontology term with ID 'GO:0000011' belong?"
# user_question="What is the source URL for the ontology term with ID 'GO:0000015'?"
# user_question="What is the term name for the ontology term with ID 'GO:0000012'?"
# user_question="Give the description for the ontology term with ID 'GO:0000014'."


# user_question = "What is the subontology of the ontology term with ID 'GO:0000011'?"
user_question = "Provide the term name and subontology for the ontology term with ID 'GO:0000022'."
# user_question = "What is the subontology of the ontology term with ID 'GO:0000015'?"
# user_question = "Give me the term name and subontology for the ontology term with ID 'GO:0000028'."


llm_generated_scheme_query = prompt_engine.generate_query(user_question, "scheme")
llm_generated_metta_query = prompt_engine.generate_query(user_question)

print("\nLLM Generated Scheme Query:\n", llm_generated_scheme_query)

print("\nLLM Generated MeTTa Query:\n", llm_generated_metta_query)

metta_query = f"!(match &self {llm_generated_metta_query})"
print("\nMeTTa Query:\n", metta_query)

metta = MeTTa()

def read_metta_file(filename):
    with open(filename, 'r') as file:
        file_content = file.read()
    return str(file_content)

metta_sample = f"""\
{read_metta_file('./metta_out/nodes.metta')}\
{read_metta_file('./metta_out/edges.metta')}\

{str(metta_query).strip()}
"""

query_result = metta.run(metta_sample)
print("\nMeTTa output:\n", query_result)


conversation = GptConversation(
    model_name="gpt-3.5-turbo",
    prompts={},
    correct=False,
)

conversation.set_api_key(
    api_key=os.getenv("OPENAI_API_KEY"), user="query_interactor"
)

out_msg, token_usage, correction = conversation.query(f"present the following result '{query_result}' for the following query '{user_question}' in a natural language if result is present  ")

print(out_msg)

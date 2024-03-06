from hyperon import MeTTa
from biochatter.prompts import BioCypherPromptEngine


prompt_engine = BioCypherPromptEngine(
                    model_name="gpt-3.5-turbo",
                    schema_config_or_info_path="./biocypher_config/schema_config.yaml",
                )
# user_question="What is the name of the compound with id 'CID499989'?"
# user_question="What is the unit value for the descriptor with id 'Molecular_Weight'?"
# user_question = "What are the descriptor ids for the compound with id 'CID2499326'?"
user_question="What is the Exact_Mass descriptor of the compound with id 'CID2499326'? In this case you can take 'Exact_Mass' as the descriptor id"

llm_generated_query = prompt_engine.generate_query(user_question)
print("\nLLM Generated Query:\n", llm_generated_query)

metta_query = f"!(match &self {llm_generated_query})"
print("\nMeTTa Query:\n", metta_query)

metta = MeTTa()

def read_metta_file(filename):
    with open(filename, 'r') as file:
        file_content = file.read()
    return str(file_content)

metta_sample = f"""\
{read_metta_file('./metta_out/compound_nodes.metta')}\
{read_metta_file('./metta_out/compound_edges.metta')}\
{read_metta_file('./metta_out/descriptor_nodes.metta')}\

{str(metta_query).strip()}
"""

print("\nMeTTa output:\n", metta.run(metta_sample))

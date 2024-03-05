from hyperon import MeTTa
from biochatter.prompts import BioCypherPromptEngine

# user_question="List the components of the compound 'CID432412'?"
# user_question="What is the name of the compound with id 'CID32145'?"
# user_question="List the descriptor attributes of the compound with id 'CID32145'?"
# user_question="What are the descriptors of compounds?"
# user_question="What are the sources for the parent relationship between compounds?"
# user_question="What is the source for descriptors of compounds?"
# user_question="What is the name of the compound with id 'CID32145'?"

# user_question = "Give me the query to get the name for the compund with CID CID2499366 VALUE "

prompt_engine = BioCypherPromptEngine(
                    model_name="gpt-3.5-turbo",
                    schema_config_or_info_path="./biocypher_config/schema_config.yaml",
                )
user_question="What is the Exact_Mass descriptor of the compound with id 'CID2499326'? In this case you can take 'Exact_Mass' as the descriptor id"
metta_query = prompt_engine.generate_query(user_question)
print("\nLLM query:\n", metta_query)

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

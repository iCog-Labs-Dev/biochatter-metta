from hyperon import MeTTa
from biochatter.prompts import BioCypherPromptEngine

# user_question="List the components of the compound 'CID432412'?"
# user_question="What is the name of the compound with id 'CID32145'?"
# user_question="List the descriptor attributes of the compound with id 'CID32145'?"
# user_question="What are the descriptors of compounds?"
# user_question="What are the sources for the parent relationship between compounds?"
# user_question="What is the source for descriptors of compounds?"
#user_question="What is the exact mass descriptor of the compound with id 'CID2498821'"


model_name = "gpt-3.5-turbo"
schema_config_or_info_dict = "./biocypher_config/schema_config.yaml"
metta_file = "./metta_out/nodes.metta"
user_question = "Give me the query to get the name for the compund with CID CID2499366 VALUE "


prompt_engine = BioCypherPromptEngine(
            model_name=model_name,
            schema_config_or_info_path=schema_config_or_info_dict,
        )


metta_query = prompt_engine.generate_query(user_question)

# query_func = agent.get_query_results
print("\n\nLLM query:\n")
print(metta_query)


metta = MeTTa()
print("\n\nMeTTa runtime:\n")
print(metta.import_file(metta_file))


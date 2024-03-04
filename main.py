from biochatter.prompts import BioCypherPromptEngine

prompts = BioCypherPromptEngine(
    schema_config_or_info_path='./biocypher_config/schema_config.yaml'
)

query = prompts.generate_query(
    # question="List the components of the compound 'CID432412'?"
    # question="What is the name of the compound with id 'CID32145'?"
    # question="List the descriptor attributes of the compound with id 'CID32145'?"
    # question="What are the descriptors of compounds?"

    # question="What are the sources for the parent relationship between compounds?"
    # question="What is the source for descriptors of compounds?"
    question="What is the exact mass descriptor of the compound with id 'CID2498821'"
)

print('----- QUERY -----')
print("!(import! ./**.metta)")
print(f"!(match &self (has-property {query})")
print('\n')
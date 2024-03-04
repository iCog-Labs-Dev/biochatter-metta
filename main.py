from biochatter.prompts import BioCypherPromptEngine
from hyperon import MeTTa

prompts = BioCypherPromptEngine(
    schema_config_or_info_path='./biocypher_config/schema_config.yaml'
)

model_name = "gpt-3.5-turbo"
schema_config_or_info_dict = "./utils/schema_config.yaml"
user_question = "Give me the query to get the name for the compund with CID CID2499366 VALUE "
metta_file = "./utils/test.metta"


prompt_engine = BioCypherPromptEngine(
            model_name=model_name,
            schema_config_or_info_path=schema_config_or_info_dict,
            # conversation_factory=conversation_factory,
        )


cypher_query = prompt_engine.generate_query(user_question)

# query_func = agent.get_query_results
print("\n\nLLM query:\n")
print(cypher_query)

# //////////////////////////////////////////////////////////


# Wanted
# !(match &self ($prop (gene ENSG00000290825) $val)
#     ($prop $val))

# Got
# MATCH (c:Compound)-[:HAS_DESCRIPTOR]->(d:Descriptor)
# RETURN c.name, d.name, d.unit, d.source, d.source_url;

# MATCH (c:Compound)-[:HAS_DESCRIPTOR]->(d:Descriptor)
# WHERE c.name = 'Aspirin'
# RETURN c.name, d.name, d.unit, d.source, d.source_url;

# MATCH (c:Compound)-[:HAS_DESCRIPTOR]->(d:Descriptor)
# WHERE c.name = 'IRX3'
# RETURN d.name, d.unit

# (match &self ($prop (Entity Compound) $val)
#     ($prop (Entity Compound) $val))


metta = MeTTa()
print("\n\nMeTTa runtime:\n")
print(metta.import_file(metta_file))

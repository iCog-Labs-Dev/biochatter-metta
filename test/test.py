entities = ['compound', 'descriptor']
rels = {
    'has_descriptor': {'source': 'compound', 'target': 'descriptor'},
    'has_attribute' : {'source': 'compound', 'target': 'descriptor'}  
    }
props = {
    'compound': {'name': True, 'id': True},
    'descriptor': {'unit': True}
    }

entities2 = ['gene', 'transcript']
rels2 = {'transcribed_to': {'source': 'gene', 'target': 'transcript'}}
rel2 = ['transcribed_to']
props2 = {'gene': {'name': 'ENSG00000206014'},
          'transcript': {'gene_name': 'ENSG00000206014', 'transcript_name': None, 'transcript_id': None, 'transcript_type': None}, 
          'relationships': {'transcribed_to': []}}

def generate_output_string(entities, rels, props):
    output = ""
    for entity in entities:
        if entity in props:
            output += f"({entity} <{entity}_id>)\n"
            for prop, value_required in props[entity].items():
                if value_required:
                    output += f"({prop} ({entity} <{entity}_id>) <{prop}_value>)\n"
                else:
                    output += f"({prop} ({entity} <{entity}_id>))\n"
        output += '\n'
        
    for rel, endpoints in rels.items():
        source = endpoints['source']
        target = endpoints['target']
        output += f"({rel} ({source} <{source}_id>) ({target} <{target}_id>))\n"
        output += f"(value ({rel} ({source} <{source}_id>) ({target} <{target}_id>)) <{rel}_value>)\n\n"

    return output

print(generate_output_string(
    entities=entities2,
    rels=rels2,
    props=props2
))

"""
(compound 'compound_id')
(name (compound 'compound_id') $"name_value")
(id (compound 'compound_id') $"id_value")

(descriptor 'descriptor_id')
(unit (descriptor 'descriptor_id') "$unit_value")

(has_descriptor ('source' 'source_id') ('target' 'target_id'))
(value (has_descriptor ('source' 'source_id') ('target' 'target_id')) '$has_descriptor_value')

(has_attrubute ('source' 'source_id') ('target' 'target_id'))
(value (has_attrubute ('source' 'source_id') ('target' 'target_id')) '$has_attribute_value')
"""








from hyperon import MeTTa


metta = MeTTa()
# metta.import_file("./metta_out/compound_edges.metta")
# op = metta.run("""
# !(import! &self ./metta_out/compound_edges.metta)

# (compound CID2499366)
# (id (compound CID2499366) "CID2499366")
# (name (compound CID2499366) "1.0")
# (source (compound CID2499366) "pubchem")
# (version (compound CID2499366) "https://pubchem.ncbi.nlm.nih.gov/rest/rdf/compound/")

# (descriptor Mono_Isotopic_Weight)
# (source_url (descriptor Mono_Isotopic_Weight) "http://semanticscience.org/resource/SIO_000008")
# (unit (descriptor Mono_Isotopic_Weight) "molar_mass_unit")
# (id (descriptor Mono_Isotopic_Weight) "Mono_Isotopic_Weight")
# (source (descriptor Mono_Isotopic_Weight) "pubchem")
# (version (descriptor Mono_Isotopic_Weight) "1.0")

# (has_descriptor (compound CID2499366) (descriptor Mono_Isotopic_Weight))
# (value (has_descriptor (compound CID2499366) (descriptor Mono_Isotopic_Weight)) 313)
# (value (has_descriptor (compound CID2499366) (descriptor Exact_Mass)) "321.266779359")
               
#  !(match &self (value (has_descriptor (compound CID2499366) (descriptor Exact_Mass)) $value)                ($value))
#           """)
# !(match &self (value (has_descriptor (compound CID2499366) (descriptor Mono_Isotopic_Weight)) $value)
#                 ($value))
# !(match &self (value (has_descriptor (compound CID2499366) (descriptor $descriptor_id)) $value)
#             ($value $descriptor_id))
# print('Test: ', op)


def read_metta_file(filename):
    with open(filename, 'r') as file:
        file_content = file.read()
    return str(file_content)

metta_query = " !(match &self (value (has_descriptor (compound CID2499326) (descriptor Exact_Mass)) $value)                ($value))"


# print(metta.run(read_metta_file('./metta_out/compound_nodes.metta')))
# metta.run(read_metta_file('./metta_out/compound_edges.metta'))
# metta.run(read_metta_file('./metta_out/descriptor_nodes.metta'))
# print(metta.run(metta_query))


metta_sample = f"""\
{read_metta_file('./metta_out/compound_nodes.metta')}\
{read_metta_file('./metta_out/compound_edges.metta')}\
{read_metta_file('./metta_out/descriptor_nodes.metta')}\

{str(metta_query).strip()}
"""
# print(metta_sample)
print("MeTTa output:", metta.run(metta_sample))


"""
 msg0 = (
            f'''Generate a database query in a query language called MeTTA, 
            here are some examples for its syntax
            
            ;Get properties of gene ENSG00000177508
            (match &self ($prop (gene ENSG00000177508) $val)
                ($prop $val))

            ;Find the transcripts of gene ENSG00000177508
            (match &self (transcribed_to (gene ENSG00000177508) $transcript)
                $transcript)

            ;What are the proteins that gene ENSG00000177508 codes for
            (match &self (, (transcribed_to (gene ENSG00000177508) $transcript)
                            (translated_to $transcript $protein))
                            $protein)

            ;Find the Gene Ontology (GO) categories associated with protein A0A024RBG1
            (match &self (go_gene_product $ontology (protein P78415))
                $ontology)

            ;Find the GO categories associated with gene ENSG00000177508
            (match &self (, (transcribed_to (gene ENSG00000177508) $transcript)
                            (translated_to $transcript $protein)
                            (go_gene_product $ontology $protein))
                            $ontology)

            ;Find biological process GO categories associated with gene ENSG00000177508
            (match &self (, (transcribed_to (gene ENSG00000177508) $transcript)
                            (translated_to $transcript $protein)
                            (go_gene_product $ontology $protein)
                            (subontology $ontology biological_process))
                            $ontology)

            ;Find pathways that gene ENSG00000177508 is a subset of
            (match &self (genes_pathways (gene ENSG00000177508) $p)
                    $p)

            ;Find pathways that gene IRX3 is a subset of (use the gene HGNC symbol instead of ensembl id)
            (match &self (, (gene_name (gene $ens) IRX3)
                            (genes_pathways (gene $ens) $p))
                    $p)

            ;Find parent pathways of the pathways that 
            ;gene IRX3 is a subset of (use the gene HGNC symbol instead of ensembl id)
            (match &self (, (gene_name (gene $ens) IRX3)
                            (genes_pathways (gene $ens) $p1)
                            (parent_pathway_of $p2 $p1))
                    $p2)

            ;What variants have eqtl association with gene IRX3
            (match &self (, (gene_name (gene $ens) IRX3)
                            (eqtl $seq $ens))
                            $seq)

            ;What variants have eqtl association with gene IRX3 and return the 
            ;properties of the association
            (match &self (, (gene_name (gene $ens) IRX3)
                            (eqtl $seq $ens)
                            ($prop (eqtl $seq $ens) $val))
                            ($prop (eqtl $seq $ens) $val))
            
            , as you are an expert in this language you will format the queries based on the example I have given you that answers'''
            f"the user's question. " 
            f"You can use the following entities: {entities}, "
            f"relationships: {list(relationships.keys())}, and "
            f"properties: {properties}. When generating the query, give entity names in lowercase."
        )

    """

# Old prompts
"""
 f"To get the properties and values for a certain entity with id 'entity_id':"
        f"($property (entity entity_id) $value)\
            ($property $value)"
        f"To get the value of a certain relationship of a source and target entity:"
        f"(value (relationship (source_entity source_entity_id) (target_entity target_entity_id)) $value)\
            ($value)"
        f"To get the list of all target entities of a relationship for a certain source entity:"
        f"(relationship (source_entity source_entity_id) (target_entity $target))\
            ($target)"
        f"The specific pattern matching queries to GO(gene ontology) should look like this for different user prompts..."
        f"To get properties of ontology term with $id:"
        f"($prop (ontology_term $id ) $val)\
            ($prop $val)"
        f"To get ontology terms related to some $term_name and retrieve their ids, descriptions, and synonyms:"
        f"(,\
                (term_name (ontology_term $id) $term_name)\
                (description (ontology_term $id) $description)\
                (synonyms (ontology_term $id) $synonyms)\
            )\
                ($id $description $synonyms)"
        f"To Retrieve ontology terms in specific sub_ontology $sub_ontology:"
        f" (,\
                (subontology (ontology_term $id) $sub_ontology)\
                (term_name (ontology_term $id) $term_name)\
            )\
                ($id $term_name)"
        f""   
        f"You should always look for the entity ids in the user's question and replace them in the query."
        f"Any entity id in the form of 'entity_id' should not exist in the query."
        f"If you don't find anything that resembles an 'id', you can put it as a variable (which has '$' in front of it) and\
            add the variable to the return value like this:\
            ($property (entity $entity_id) $value)\
            ($property $value $entity_id)"
        f"You can use the following entities: {entities}, "
        f"relationships: {list(relationships.keys())}, and "
        f"properties: {properties}."
        f"Write a pattern matching query for the user's question"

"""
def generate_sample_metta_string(entities, relationships, properties) -> str:
    output = ""
    for entity in entities:
        if entity in properties:
            output += f"({entity} {entity}_id)\n"
            for prop, value_required in properties[entity].items():
                if value_required:
                    output += f"({prop} ({entity} {entity}_id) ${prop}_value)\n"
                else:
                    output += f"({prop} ({entity} {entity}_id))\n"
        output += '\n'
        
    for rel, endpoints in relationships.items():
        source = endpoints['source']
        target = endpoints['target']
        output += f"({rel} ({source} {source}_id) ({target} {target}_id))\n"
        output += f"(value ({rel} ({source} {source}_id) ({target} {target}_id)) ${rel}_value)\n\n"

    return output

def get_metta_prompt(entities, relationships, properties) -> str:

    sample_metta_string = generate_sample_metta_string(
            entities=list(entities),
            relationships=dict(relationships),
            properties=dict(properties)
        )
    
    prompt = (
        # f"I have a datastore that looks like this:"
        # f"{sample_metta_string}\n"
        f"You will generate Scheme queries for this datastore based on the following examples:"

        f"""
            ;Get properties of #ENTITY #ENTITY_ID
            ***
                ($prop (#ENTITY #ENTITY_ID) $val)
                ($prop $val)
            ***

            ;Get properties of #ENTITY with some #PROPERTY_NAME with #PROPERTY_VALUE
            ***
                (,
                    (#PROPERTY_VALUE (#ENTITY #ENTITY_ID) #PROPERTY_NAME)
                    ($prop (#ENTITY #ENTITY_ID) $val)
                )
                ($prop $val)
            ***

            ;Find the a #RELATIONSHIP of some #ENTITY #ENTITY_ID
            ***
                (#RELATIONSHIP (#ENTITY #ENTITY_ID) $#ENTITY)
                $#ENTITY
            ***

            ;Find #ENTITY-1 who has a #RELATIONSHIP with #ENTITY-2 with #PROPERTY_NAME #PROPERTY_VALUE
            ***
                (,
                    (#PROPERTY_NAME (#ENTITY-2 $var) #PROPERTY_VALUE)
                    (#RELATIONSHIP (#ENTITY-2 $var) $#ENTITY-1)
                )
                $#ENTITY-1
            ***

        """

        f"Everything between the three asterisks (*** .... ***) is a query."
        f"You must replace #ENTITY with one of these entity terms: {entities}, "
        f"You must replace #RELATIONSHIP with one of these relationship terms: {list(relationships.keys())}, and "
        f"You must replace #PROPERTY_NAME with one of these property name terms: {properties}."

        f"#PROPERTY_VALUE is the value for the #PROPERTY_NAME and should be provided in the user's question"
        f"You should always look for the #ENTITY_ID or #PROPERTY_VALUE in the user's question."
        f"The #ENTITY_ID or #PROPERTY_VALUE must not be surrounded with quoted in the query."

        f"If you think any matching entity, relationship or property is missing from the lists I gave you or from the user's question,\
             you can represent them as a variable in the query like this: $entity | $entity_id | $relationship | $property_name | $property_value"
        f"If you don't find anything that matches the #ENTITY_ID or #PROPERTY_VALUE, you can represent them as variables in the query\
            like this: $entity_id | $property_value"

        f"You should always "
        f"Based on the information given to you above, you will write a pattern matching query for the user's question"
    )

    return prompt




 
"""

            ;Find the Gene Ontology (GO) categories associated with protein A6NIX2
            (match &space
                (
                    go_gene_product $ontology (protein A6NIX2)
                )
                $ontology
            )

            ;Find the  Gene Ontology (GO) categories associated with gene ENSG00000177508
            (match &space
                (,
                    (transcribed_to (gene ENSG00000177508) $transcript)
                    (translates_to $transcript $protein)
                    (go_gene_product $ontology $protein)
                )
                $ontology
            )

            ;Find biological process GO categories associated with gene FNIP2 (use the gene HGNC symbol instead of ensembl id)
            (match &space
                (,
                    (gene_name (gene $ens) FNIP2)
                    (transcribed_to (gene $ens) $transcript)
                    (translates_to $transcript $protein)
                    (go_gene_product $ontology $protein)
                    (subontology $ontology biological_process)
                )
                $ontology
            )

            ;Find pathways that gene ENSG00000177508 is a subset of
            (match &space
                (genes_pathways (gene ENSG00000177508) $p)
                $p
            )

            ;Find pathways that gene IRX3 is a subset of (use the gene HGNC symbol instead of ensembl id)
            (match &space
                (,
                    (gene_name (gene $ens) IRX3)
                    (genes_pathways (gene $ens) $p)
                )
                $p
            )

             ;Find parent pathways of the pathways that gene TFAP2A is a subset of (use the gene HGNC symbol instead of ensembl id)
            (match &space
                (,
                    (gene_name (gene $ens) TFAP2A)
                    (genes_pathways (gene $ens) $p1)
                    (parent_pathway_of $p2 $p1)
                )
                $p2
            )

            ;What variants have eqtl association with gene IRX3 (use the gene HGNC symbol instead of ensembl id)
            (match &space
                (,
                    (gene_name (gene $ens) IRX3)
                    (eqtl $seq (gene $ens))
                )
                $seq
            )

            ;What variants have eqtl association with gene POLR3K (use the gene HGNC symbol instead of ensembl id)
            (match &space
                (,
                    (gene_name (gene $ens) POLR3K)
                    (eqtl $seq (gene $ens))
                )
                $seq
            )

            ;What variants have eqtl association with gene IRX3 (use the gene HGNC symbol instead of ensembl id) and return the properties of the association
            (match &space
                (,
                    (gene_name  $ens IRX3)
                    (eqtl $seq $ens)
                    ($prop (eqtl $seq $ens) $val)
                )
                ($prop (eqtl $seq $ens) $val)
            )

            ;What variants have eqtl association with gene ENSG00000170540 and return the properties of the association
            (match &space
                (,
                    (eqtl $seq (gene ENSG00000170540))
                    ($prop (eqtl $seq (gene ENSG00000170540)) $val)
                )
                ($prop (eqtl $seq (gene ENSG00000170540)) $val)
            )


            ;Find molecular function Gene Ontology (GO) categories associated with gene FLRT2 (use the gene HGNC symbol instead of ensembl id)
            (match &space
                (,
                    (gene_name (gene $ens) FLRT2)
                    (transcribed_to (gene $ens) $transcript)
                    (translates_to $transcript $protein)
                    (go_gene_product $ontology $protein)
                    (subontology $ontology molecular_function)
                )
                $ontology
            )

            ;Find cellular component Gene Ontology (GO) categories associated with gene ENSG00000185070
            (match &space
                (,
                    (transcribed_to (gene ENSG00000185070) $transcript)
                    (translates_to $transcript $protein)
                    (go_gene_product $ontology $protein)
                    (subontology $ontology cellular_component)
                )
                $ontology
            )

            ;Please provide the properties of the eqtl association involving the rs224167 variant and the gene ENSG00000234769
            (match &space
                (,
                    ($prop (eqtl  (sequence_variant rs224167) (gene ENSG00000234769)) $val)
                )
            ($prop (eqtl (sequence_variant rs224167) (gene ENSG00000234769)) $val)
            )

        """
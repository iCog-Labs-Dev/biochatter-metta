class MettaPrompt:

    def __init__(self, entities, relationships, properties, schema_nodes, schema_edges) -> None:
        self.entities = entities
        self.relationships = relationships
        self.properties = properties
        self.schema_nodes = schema_nodes
        self.schema_edges = schema_edges

    def generate_metta_node_samples(self) -> str:
        if not self.schema_nodes:
            return ''
        
        msg = "\nThe following are the representations of the nodes in the dataset: \n###\n"

        for input_label, properties in self.schema_nodes.items():
            msg += f"; This is the format of the nodes for '{input_label}': \n"
            msg += f"({input_label} <{input_label}_id>)\n"
            for prop, prop_type in properties.items():
                # Skip propeties that are not usually mapped to the MeTTa files
                if prop in ['source', 'source_url', 'version']:
                    continue
                msg += f"({prop} ({input_label} <{input_label}_id>) <value_of_type_{prop_type}>)\n"
    
        msg += "### \n"
        return msg

    def generate_metta_edge_samples(self):
        if not self.schema_edges:
            return ''
        
        msg = "\nThe following are the representations of the edges in the dataset: \n###\n"

        for input_label, attributes in self.schema_edges.items():
            source = attributes['source']
            target = attributes['target']
            properties = attributes['properties']

            description = attributes.get('description', None)
            full_name = attributes.get('full_name', None)

            if full_name: msg += f"; The name '{input_label}' is just a short form of \"{full_name}\". \n"
            if description: msg += f"; The relationship '{input_label}' would be described as: \"{description}\". \n"
            msg += f"; These is the format of the edges for '{input_label}': \n"
            msg += f"({input_label} ({source} <{source}_id>) ({target} <{target}_id>))"
            for prop, prop_type in properties.items():
                # Skip propeties that are not usually mapped to the MeTTa files
                if prop in ['source', 'source_url', 'version']:
                    continue
                msg += f"({prop} ({input_label} ({source} <{source}_id>) ({target} <{target}_id>)) <value_of_type_{prop_type}>)\n"
    
        msg += "### \n"
        return msg


    def get_metta_prompt(self) -> str:

        metta_nodes = self.generate_metta_node_samples()
        metta_edges = self.generate_metta_edge_samples()
        
        prompt = (
            f"I have a dataset for storing biology data using a lisp style syntax."
            f"The dataset is classified into 'nodes' and 'edges' as follows:"
            f"{metta_nodes}\n"
            f"{metta_edges}\n"
            f"You will generate Scheme-like queries for this dataset that will answer the user's question."
            f"You can refer to the following examples to construct the queries:"

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

            f"Everything between the three hashtags (### .... ###) is the exact format of the dataset."
            f"Everything between the three asterisks (*** .... ***) is a query."
            f"Everything between angle brackets (<..>) is a variable that should either be replaced by what is found in \
                the user's question or should be pattern matched and returned back to the user."

            # f"You must replace #ENTITY with one of these entity terms: {self.entities}, "
            # f"You must replace #RELATIONSHIP with one of these relationship terms: {list(self.relationships.keys())}, and "
            # f"You must replace #PROPERTY_NAME with one of these property name terms: {self.properties}."

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
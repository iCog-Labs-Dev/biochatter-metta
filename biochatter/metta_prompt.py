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
        
        metta_node_sample = "\nThe following are the representations of the nodes in the dataset: \n###\n"

        for node_label, properties in self.schema_nodes.items():
            metta_node_sample += f"; This is the format of the nodes for '{node_label}': \n"
            metta_node_sample += f"({node_label} <{node_label}_id>)\n"
            for prop, prop_type in properties.items():
                # Skip propeties that are not usually mapped to the MeTTa files
                if prop in ['source', 'source_url', 'version']:
                    continue
                metta_node_sample += f"({prop} ({node_label} <{node_label}_id>) <value_of_type_{prop_type}>)\n"
    
        metta_node_sample += "### \n"
        return metta_node_sample

    def generate_metta_edge_samples(self):
        if not self.schema_edges:
            return ''
        
        metta_edge_sample = "\nThe following are the representations of the edges in the dataset: \n###\n"

        for edge_label, attributes in self.schema_edges.items():
            source = attributes['source']
            target = attributes['target']
            properties = attributes['properties']

            description = attributes.get('description', None)
            full_name = attributes.get('full_name', None)

            if full_name: metta_edge_sample += f"; The name '{edge_label}' is just a short form of \"{full_name}\". \n"
            if description: metta_edge_sample += f"; The relationship '{edge_label}' would be described as: \"{description}\". \n"
            metta_edge_sample += f"; These is the format of the edges for '{edge_label}': \n"
            metta_edge_sample += f"({edge_label} ({source} <{source}_id>) ({target} <{target}_id>))\n"
            for prop, prop_type in properties.items():
                # Skip propeties that are not usually mapped to the MeTTa files
                if prop in ['source', 'source_url', 'version']:
                    continue
                metta_edge_sample += f"({prop} ({edge_label} ({source} <{source}_id>) ({target} <{target}_id>)) <value_of_type_{prop_type}>)\n"
    
        metta_edge_sample += "### \n"
        return metta_edge_sample
    
    def generate_metta_node_query_samples(self):
        if not self.schema_nodes:
            return ''
        
        node_query_samples = "\nThe following are sample queries for the nodes in the dataset: \n***\n"

        for node_label, properties in self.schema_nodes.items():
            node_query_samples += f"\n; Get properties of a '{node_label}' with some id <{node_label}_id>: \n\
                                        ($prop ({node_label} <{node_label}_id>) $val)\n\
                                        ($prop $val)\n"

            for prop, _ in properties.items():
                # Skip propeties that are not usually mapped to the MeTTa files
                if prop in ['source', 'source_url', 'version']:
                    continue

                node_query_samples += f"\n; Get the '{prop}' property of some '{node_label}' with id <{node_label}_id>: \n\
                                            ({prop} ({node_label} <{node_label}_id>) $val)\n\
                                            ($val)\n"

                node_query_samples += f"\n; Get the properties of a '{node_label}' with '{prop}' of <some_{prop}_val>: \n\
                                            (,\n\
                                             ({prop} ({node_label} $id) <some_{prop}_val>)\n\
                                             ($prop ({node_label} $id) $val)\n\
                                            )\n\
                                            ($prop $val)\n"
    
        node_query_samples += "*** \n"
        return node_query_samples

    def generate_metta_edge_query_samples(self):
        if not self.schema_edges:
            return ''
        
        edge_query_samples = "\nThe following are sample queries for the edges in the dataset: \n***\n"

        for edge_label, attributes in self.schema_edges.items():
            source = attributes['source']
            target = attributes['target']
            properties = attributes['properties']

            edge_query_samples += f"; Find the '{target} nodes' of the '{source}' with id <{source}_id>:\n\
                                    ({edge_label} ({source} <{source}_id>) ${target}_node)\n\
                                    (${target}_node)\n"

            for prop, prop_type in properties.items():
                # Skip propeties that are not usually mapped to the MeTTa files
                if prop in ['source', 'source_url', 'version']:
                    continue

                edge_query_samples += f"; Find the '{target} nodes' of a '{source}' with '{prop}' of <some_{prop}_val>:\n\
                                        (,\n\
                                         ({prop} ({source} $id) <some_{prop}_val>)\n\
                                         ({edge_label} ({source} $id) ${target}_node)\n\
                                        )\n\
                                        (${target}_node)\n"

        edge_query_samples += "*** \n"
        return edge_query_samples

    def get_metta_prompt(self) -> str:

        metta_node_samples = self.generate_metta_node_samples()
        metta_edge_samples = self.generate_metta_edge_samples()

        metta_node_query_samples = self.generate_metta_node_query_samples()
        metta_edge_query_samples = self.generate_metta_edge_query_samples()
        
        prompt = (
            f"I have a dataset for storing biology data using a lisp style syntax."
            f"The dataset is classified into 'nodes' and 'edges' as follows:"
            f"{metta_node_samples}\n"
            f"{metta_edge_samples}\n"

            f"You will generate Scheme-like queries for this dataset that will answer the user's question."
            f"The query will have two outer parenthesis. The first one will contain the pattern matching query\
                on the dataset, and the second one will contain the variables to be returned by the query."
            f"You can refer to the following examples for constructing the queries:"
            f"{metta_node_query_samples}\n"
            f"{metta_edge_query_samples}\n"

            f"Everything between the three hashtags (### .... ###) is the exact format of the dataset."
            f"Everything between the three asterisks (*** .... ***) is a query."
            f"Everything between angle brackets (<..>) is a variable that should either be replaced with the appropriate\
                'id' or 'value' found in the user's question or should be replaced with a vairable to be returned by the query."
            f"The word after the dollar sign ($) is a variable that can replace values that aren't provided by the user or\
                unknown values that are requested by the user."

            # f"You may only use these entity terms: {self.entities}, "
            # f"You may only use these relationship terms: {list(self.relationships.keys())}, and "
            # f"You may only use these property name terms: {self.properties}."

            # f"#PROPERTY_VALUE is the value for the #PROPERTY_NAME and should be provided in the user's question"
            # f"You should always look for the #ENTITY_ID or #PROPERTY_VALUE in the user's question."
            # f"The #ENTITY_ID or #PROPERTY_VALUE must not be surrounded with quoted in the query."

            # f"If you think any matching entity, relationship or property is missing from the lists I gave you or from the user's question,\
            #     you can represent them as a variable in the query like this: $entity | $entity_id | $relationship | $property_name | $property_value"
            # f"If you don't find anything that matches the #ENTITY_ID or #PROPERTY_VALUE, you can represent them as variables in the query\
            #     like this: $entity_id | $property_value"

            f"Based on the information given to you above, you will write a pattern matching query on the dataset for the user's question."
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
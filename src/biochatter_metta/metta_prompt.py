import json

class MettaPrompt:

    def __init__(self, schema_nodes, schema_edges) -> None:
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
            

            f"Example queries that are given above contain both complex and simple queries. Examples that start with ',' are complex queries those that don't contains ',' are simple queries."
            f"Complex queries propagate variable values through expression from the top to the bottom. for example let's look at the below complex query\n\
                  (,\n\
                        (gene_name (gene $ens) <some_gene_name_value>)\n\
                        (transcribed_to (gene $ens) $transcript)\n\
                        (translates_to $transcript $protein)\n\
                        (go_gene_product $ontology $protein)\n\
                        (subontology $ontology <some_subontology_val>)\n\
                    )\n\
                    ($ontology)\n\
            from '(gene_name (gene $ens) <some_gene_name_value>)' expression, the value $ens will be retrived and will be passed to '(transcribed_to (gene $ens) $transcript)'.\
            The same way, from '(transcribed_to (gene $ens) $transcript)' the value of $transcript will be retrived and will be passed to '(translates_to $transcript $protein)'.\
            Again, from '(translates_to $transcript $protein)' $protien will be retrieved and will be passed to '(go_gene_product $ontology $protein)'.\
            Finally, from '(go_gene_product $ontology $protein)', $ontology will be retrieved and will be passed to '(subontology $ontology <some_subontology_val>)'. At the end value of $ ontology will be returned."
            f"Simple queries just pattern match a single experession and then return the result. Let's look at one example\n\
                (\n\
                        go_gene_product $ontology (protein <some_protien_name_value>)\n\
                    )\n\
                    ($ontology)\n\
            The above example just pattern match the given expression and return the value of $ontology."
            f"Everything between the three hashtags (### .... ###) is the exact format of the dataset."
            f"Everything between the three asterisks (*** .... ***) is a query."
            f"Everything between angle brackets (<..>) is a variable that should either be replaced with the appropriate\
                'id' or 'value' found in the user's question or should be replaced with a vairable to be returned by the query."\
            f"For example, let's look at some user questions and their corresponding query.\
                'Give the description for the ontology term with ID 'GO:0000785''.\
            for the above user question, the below query can be generated\n\
                (description (ontology_term GO:0000785) $val)\n\
                 ($val)\n\
            let's look at other user question that requires complex query to be genrated.\
            'Find all properties of genes that belong into biological process subontology.'\n\
            (,\n\
                (subontology (ontology_term $id) biological_process)\n\
                ($prop (ontology_term $id) $val)\n\
                )\n\
                ($prop $val)\n\
            "
            f"The word after the dollar sign ($) is a variable that can replace values that aren't provided by the user or\
                unknown values that are requested by the user."
            f"The 'id' or 'value' you find in the user's question should be treated as symbols and must not be wrapped in quotes."
            f"Return only query,  no explanation and other texts"
            f"Based on the information given to you above, you will write a pattern matching query on the dataset for the user's question."
        )
        return prompt
    
    def wrap_metta_query(self, metta_query, space='self'):
        return f"!(match &{space} \n {metta_query} \n)"


    def get_metta_imports(self, schema_mappings, space='self'):
        metta_path = []

        with open(schema_mappings) as file:
            mappings = json.load(file)

            # Edge MeTTa Files
            source_target_nodes = []    # Also import the source and target nodes from the edges
            for edge_label in self.schema_edges.keys():
                edge_schema = mappings['edges'].get(edge_label, '')
                if not edge_schema:
                    continue
                edge_path = edge_schema['metta_location']
                
                source_target_nodes.append(edge_schema['source'])
                source_target_nodes.append(edge_schema['target'])

                if edge_path and edge_path not in metta_path:
                    metta_path.append(edge_path)

            # Node MeTTa Files
            node_labels = list(self.schema_nodes.keys()) + source_target_nodes
            for node_label in node_labels:
                node_schema = mappings['nodes'].get(node_label, '')
                if not node_schema:
                    continue
                node_path = node_schema['metta_location']

                if node_path and node_path not in metta_path:
                    metta_path.append(node_path)
        
        # Remove the dot('.') that the paths start with
        metta_path = [path[1:] if path.startswith('.') else path for path in metta_path]

        return '\n'.join(
            [f'!(import! &{space} {path})' for path in metta_path]
        )
        


            
        # open schema mappings, read json
        # select the metta file paths based on the nodes and edges
        # compile them using the load-ascii/import function
        pass
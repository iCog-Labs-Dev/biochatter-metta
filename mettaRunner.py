from hyperon import MeTTa

metta = MeTTa()

def read_metta_file(filename):
    with open(filename, 'r') as file:
        file_content = file.read()
    return str(file_content)

metta_sample = f"""\
{read_metta_file('./metta_out/edges.metta')}\
{read_metta_file('./metta_out/nodes.metta')}

"""
# print(metta_sample)
query_result = metta.run(metta_sample)
print("\nMeTTa output:\n", query_result)
from typing import Tuple, Set
from models import Literal, Clause, KnowledgeBase

def parse_literal(lit_str):
    """
    Parses a literal string into a Literal object.

    Args:
        lit_str (str): The literal string to parse.

    Returns:
        Literal: An instance of Literal with the symbol and negation flag.
    """
    lit_str = lit_str.strip()
    if lit_str.startswith('-'):
        return Literal(symbol=lit_str[1:], negation=True)
    else:
        return Literal(symbol=lit_str, negation=False)

def parse_clause(clause_str):
    """
    Parses a clause string into a Clause object.

    Args:
        clause_str (str): A string representing the clause, with literals separated by 'OR'.

    Returns:
        Clause: A Clause object containing a set of parsed literals.
    """
    literals = [parse_literal(lit) for lit in clause_str.split('OR')]
    return Clause(set(literals))

def read_input_file(filename):
    """
    Reads and parses the input file to extract the alpha clause and construct a KnowledgeBase.
    Parameters:
        filename (str): The path to the input file.
    Returns:
        tuple:
            - alpha_clause: The parsed alpha clause from the first line of the file.
            - KB (KnowledgeBase): The knowledge base populated with clauses from the file.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    lines = [line.strip() for line in lines if line.strip()]
    
    alpha_str = lines[0]
    n = int(lines[1])
    clause_strs = lines[2:2 + n]
    
    alpha_clause = parse_clause(alpha_str)
    
    KB = KnowledgeBase()
    for clause_str in clause_strs:
        clause = parse_clause(clause_str)
        KB.add_clause(clause)
    
    return alpha_clause, KB

def negate_clause(clause):
    """
    Negates a given clause by negating each of its literals.

    Args:
        clause (Clause): The clause to negate.

    Returns:
        Set[Clause]: A set of negated clauses.
    """
    negated_clauses = set()
    for literal in clause.literals:
        negated_clauses.add(Clause({literal.negate()}))
        
    return negated_clauses

def write_output_file(filename, steps, entails):
    """
    Writes the output to a specified file.
    This function takes a filename, a list of steps, and an entails flag to write the output in a specific format.
    Each step's clauses are written with their length followed by the sorted clauses.
    At the end, "YES" or "NO" is written based on the entails flag.
    Parameters:
        filename (str): The path to the output file.
        steps (List[List[str]]): A list of steps, where each step is a list of clauses.
        entails (bool): A flag indicating whether entails is true or false.
    Returns:
        None
    """
    with open(filename, 'w') as f:
        for step_clauses in steps:
            f.write(f"{len(step_clauses)}\n")
            if step_clauses:
                sorted_clauses = sorted(step_clauses, key=str)
                for clause in sorted_clauses:
                    f.write(f"{clause}\n")
        
        f.write("YES" if entails else "NO")

from models import Clause, KnowledgeBase
from utils import negate_clause
from itertools import combinations

def pl_resolve(A, B):
    """
    Perform the resolution rule on two clauses A and B.
    The resolution rule is used in propositional logic to infer new clauses
    by combining two clauses that contain complementary literals.
    Args:
        A (Clause): The first clause.
        B (Clause): The second clause.
    Returns:
        set: A set of new clauses (resolvents) obtained by resolving A and B.
    Example:
        >>> A = Clause({Literal('P'), Literal('Q')})
        >>> B = Clause({Literal('P').negate(), Literal('R')})
        >>> resolvents = pl_resolve(A, B)
        >>> print(resolvents)
        {Clause({Literal('Q'), Literal('R')})}
    Note:
        - The function assumes that the Clause and Literal classes have been
          defined with appropriate methods such as `negate`, `union`, and
          `is_tautology`.
        - The function does not handle cases where A or B are not valid clauses.
    """
    resolvents = set()
    
    for a in A.literals:
        for b in B.literals:
            if a == b.negate():
                new_literals = A.literals.union(B.literals) - {a, b}
                new_clause = Clause(new_literals)
                
                if not new_clause.is_tautology():
                    resolvents.add(new_clause)
                    
    return resolvents

def pl_resolution(KB, alpha):
    """
    Perform the resolution algorithm to check if a knowledge base (KB) entails a given clause (alpha).
    Args:
        KB (KnowledgeBase): The knowledge base containing a set of clauses.
        alpha (Clause): The clause to be tested for entailment.
    Returns:
        tuple: A tuple containing a boolean indicating whether KB entails alpha, and a list of sets of new clauses generated in each iteration.
    Example:
        >>> KB = KnowledgeBase({Clause({Literal('P')}), Clause({Literal('Q')})})
        >>> alpha = Clause({Literal('R')})
        >>> entails, loop_results = pl_resolution(KB, alpha)
        >>> print(entails)
        False
    Note:
        - The function assumes that the KnowledgeBase, Clause, and Literal classes have been defined with appropriate methods such as `get_clauses`, `negate_clause`, and `is_tautology`.
        - The function does not handle cases where KB or alpha are not valid.
    """
    # Initialize the set of clauses with the clauses from KB and the negation of alpha
    clauses = KB.get_clauses().union(negate_clause(alpha))
    seen_clauses = set(clauses)
    loop_results = []
    
    while True:
        new = set()
        # Process all possible pairs of clauses
        for ci, cj in combinations(clauses, 2):
            resolvents = pl_resolve(ci, cj)
            
            # Add all valid resolvents first
            for resolvent in resolvents:
                if resolvent not in seen_clauses and not resolvent.is_tautology():
                    new.add(resolvent)
        
        # Check for the empty clause (indicating a contradiction)
        for clause in new:
            if not clause.literals:
                loop_results.append(new)
                return True, loop_results
                
        # If no new clauses are generated, return False
        if not new:
            loop_results.append(new)
            return False, loop_results
            
        # Update the sets of seen and current clauses
        loop_results.append(new)
        seen_clauses.update(new)
        clauses.update(new)
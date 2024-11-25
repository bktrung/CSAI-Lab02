from typing import Set

class Literal:
    """
    Class: Literal
    Represents a logical literal with a symbol and its negation state.
    Attributes:
        symbol (str): The symbol of the literal.
        negation (bool): Indicates whether the literal is negated.
    Methods:
        __init__(self, symbol, negation):
            Initializes the Literal with the given symbol and negation status.
        __repr__(self):
            Returns the string representation of the Literal.
        __eq__(self, other):
            Checks equality with another Literal.
        __hash__(self):
            Returns the hash based on symbol and negation.
        negate(self):
            Returns a new Literal with the negation state toggled.
    """
    def __init__(self, symbol, negation):
        self.symbol = symbol
        self.negation = negation
        
    def __repr__(self):
        return f'-{self.symbol}' if self.negation else self.symbol
    
    def __eq__(self, other):
        if not isinstance(other, Literal):
            return NotImplemented
        return self.symbol == other.symbol and self.negation == other.negation
    
    def __hash__(self):
        return hash((self.symbol, self.negation))
    
    def negate(self):
        return Literal(self.symbol, not self.negation)
    
    
class Clause:
    """
    Clause represents a logical clause consisting of a set of literals.
    Attributes:
        literals (frozenset): A frozenset containing the literals in the clause.
    Methods:
        __init__(literals):
            Initializes a Clause instance with the given literals.
        __repr__():
            Returns a string representation of the clause, with literals sorted and joined by " OR ".
        __eq__(other):
            Checks equality with another Clause instance based on the literals.
        __hash__():
            Returns a hash based on the literals, allowing Clause instances to be used in sets and as dictionary keys.
        is_tautology():
            Determines if the clause is a tautology, i.e., it contains both a literal and its negation.
    """
    def __init__(self, literals):
        self.literals = frozenset(literals)

    def __repr__(self):
        if not self.literals:
            return "{}"
        sorted_literals = sorted(self.literals, key=lambda x: (x.symbol, x.negation))
        return " OR ".join(repr(lit) for lit in sorted_literals)

    def __eq__(self, other):
        if not isinstance(other, Clause):
            return NotImplemented
        return self.literals == other.literals

    def __hash__(self):
        return hash(self.literals)

    def is_tautology(self):
        symbols = {}
        for literal in self.literals:
            if literal.symbol in symbols:
                if symbols[literal.symbol] != literal.negation:
                    return True
            else:
                symbols[literal.symbol] = literal.negation
        return False
    
    
class KnowledgeBase:
    """
    Class KnowledgeBase manages a collection of clauses, providing functionality to add new clauses,
    check for the existence of a clause, retrieve all clauses, and iterate over them.
    Attributes:
        clauses (set): A set containing Clause instances representing the knowledge base.
    Methods:
        __init__(self, clauses=None):
            Initializes the KnowledgeBase with an optional iterable of clauses.
        add_clause(self, clause: Clause) -> bool:
            Adds a clause to the knowledge base if it is not a tautology and not already present.
        contains(self, clause: Clause) -> bool:
            Checks whether a specific clause exists in the knowledge base.
        get_clauses(self) -> set:
            Retrieves all clauses stored in the knowledge base.
        __str__(self) -> str:
            Returns a string representation of the knowledge base, listing all clauses.
        __iter__(self):
            Returns an iterator to allow iteration over the clauses in the knowledge base.
        size(self) -> int:
            Returns the number of clauses in the knowledge base.
    """
    def __init__(self, clauses = None):
        self.clauses = set(clauses) if clauses else set()

    def add_clause(self, clause: Clause):
        if not clause.is_tautology() and clause not in self.clauses:
            self.clauses.add(clause)
            return True
        return False

    def contains(self, clause: Clause):
        return clause in self.clauses

    def get_clauses(self):
        return self.clauses

    def __str__(self):
        if not self.clauses:
            return "KB is empty"
        return "\n".join(str(clause) for clause in sorted(self.clauses, key=lambda c: str(c)))

    def __iter__(self):
        return iter(self.clauses)

    def size(self):
        return len(self.clauses)
from collections import defaultdict 

def read_grammar(filename): 
    grammar = defaultdict(list) 
    with open(filename, 'r') as f: 
        for line in f: 
            if '->' in line: 
                lhs, rhs = line.strip().split('->') 
                productions = [p.strip().split() for p in rhs.split('|')] 
                grammar[lhs.strip()].extend(productions) 
    return grammar 

def eliminate_left_recursion(grammar): 
    new_grammar = defaultdict(list) 
    for nt in grammar: 
        alpha = [p[1:] for p in grammar[nt] if p and p[0] == nt] 
        beta = [p for p in grammar[nt] if not p or p[0] != nt] 
        if alpha: 
            new_nt = nt + "'" 
            new_grammar[nt] = [p + [new_nt] for p in beta] if beta else [[new_nt]] 
            new_grammar[new_nt] = [p + [new_nt] for p in alpha] + [['ε']] 
        else: 
            new_grammar[nt] = grammar[nt] 
    return new_grammar 

def print_grammar(grammar): 
    for nt in grammar: 
        rhs = [' '.join(p) for p in grammar[nt]] 
        print(f"{nt} -> {' | '.join(rhs)}") 

def main(): 
    filename = "grammar.txt" 
    print("Original Grammar:") 
    grammar = read_grammar(filename) 
    print_grammar(grammar) 
    print("\nGrammar after Left Recursion Elimination:") 
    updated_grammar = eliminate_left_recursion(grammar) 
    print_grammar(updated_grammar) 

if __name__ == " main ": 
    main()

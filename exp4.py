EPSILON = '#'
END_MARKER = '$'

def parse_grammar(filename="4.txt"):
    grammar = {}
    non_terminals = set()
    terminals = set()
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
        return {}, set(), set(), None
    start_symbol = lines[0].split('->')[0].strip()
    for line in lines:
        left, right = line.split('->')
        left = left.strip()
        productions = [p.strip().split() for p in right.split('|')]
        grammar[left] = productions
        non_terminals.add(left)

        for prod in productions:
            for symbol in prod:
                if not symbol.isupper() and symbol != EPSILON:
                    terminals.add(symbol)
    terminals -= non_terminals
    return grammar, non_terminals, terminals, start_symbol

def compute_first(grammar, non_terminals):
    first = {nt: set() for nt in non_terminals}
    changed = True
    while changed:
        changed = False
        for nt in non_terminals:
            for production in grammar[nt]:
                for symbol in production:
                    if symbol not in non_terminals:
                        if symbol not in first[nt]:
                            first[nt].add(symbol)
                            changed = True
                        break
                else:
                    before = len(first[nt])
                    first[nt].update(first[symbol] - {EPSILON})
                    if EPSILON not in first[symbol]:
                        break
                    if len(first[nt]) > before:
                        changed = True
            else:
                if EPSILON not in first[nt]:
                    first[nt].add(EPSILON)
                    changed = True
    return first

def compute_follow(grammar, non_terminals, start_symbol, first):
    follow = {nt: set() for nt in non_terminals}
    follow[start_symbol].add(END_MARKER)
    changed = True
    while changed:
        changed = False
        for A in non_terminals:
            for production in grammar[A]:
                for i, B in enumerate(production):
                    if B in non_terminals:
                        beta = production[i + 1:]

                        first_beta = set()
                        if not beta:
                            first_beta.add(EPSILON)
                        else:
                            for symbol in beta:
                                if symbol in non_terminals:
                                    first_beta.update(first[symbol] - {EPSILON})
                                    if EPSILON not in first[symbol]:
                                        break
                                else:
                                    first_beta.add(symbol)
                                    break
                            else:
                                first_beta.add(EPSILON)

                        before = len(follow[B])
                        follow[B].update(first_beta - {EPSILON})
                        if EPSILON in first_beta:
                            follow[B].update(follow[A])
                        if len(follow[B]) > before:
                            changed = True
    return follow

def display_sets(title, sets):
    print(f"\n--- {title} ---")
    for nt in sorted(sets):
        elements = ', '.join(sorted(sets[nt]))
        print(f"{title.split()[0]}({nt}) = {{ {elements} }}")

def main():
    grammar, non_terminals, terminals, start_symbol = parse_grammar()
    if not grammar:
        return
    first_sets = compute_first(grammar, non_terminals)
    display_sets("FIRST Sets", first_sets)
    follow_sets = compute_follow(grammar, non_terminals, start_symbol, first_sets)
    display_sets("FOLLOW Sets", follow_sets)

if __name__ == "__main__":
    main()

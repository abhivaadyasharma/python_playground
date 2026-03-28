#Author: Abhivaadya Sharma

"""
Periodic Table CLI (118 elements) + Molar Mass Calculator
Usage: This program helps to find elements using thier atomic number, element symbol and element name. It also helps you calculate molar mass.
"""
import sympy as sp
import random
from dataclasses import dataclass
import re
from typing import Dict, Tuple, List

@dataclass(frozen=True)
class Element:
    Z: int
    symbol: str
    name: str
    atomic_mass: float  # standard atomic weight (approx; for educational use)

# --- Full list of 118 elements ---
# Atomic masses are standard values (rounded) suitable for most calculations.
ELEMENTS_LIST: List[Element] = [
    Element(1,"H","Hydrogen",1.008),
    Element(2,"He","Helium",4.0026),
    Element(3,"Li","Lithium",6.94),
    Element(4,"Be","Beryllium",9.0122),
    Element(5,"B","Boron",10.81),
    Element(6,"C","Carbon",12.011),
    Element(7,"N","Nitrogen",14.007),
    Element(8,"O","Oxygen",15.999),
    Element(9,"F","Fluorine",18.998),
    Element(10,"Ne","Neon",20.1797),
    Element(11,"Na","Sodium",22.990),
    Element(12,"Mg","Magnesium",24.305),
    Element(13,"Al","Aluminium",26.982),
    Element(14,"Si","Silicon",28.085),
    Element(15,"P","Phosphorus",30.974),
    Element(16,"S","Sulfur",32.06),
    Element(17,"Cl","Chlorine",35.45),
    Element(18,"Ar","Argon",39.948),
    Element(19,"K","Potassium",39.098),
    Element(20,"Ca","Calcium",40.078),
    Element(21,"Sc","Scandium",44.956),
    Element(22,"Ti","Titanium",47.867),
    Element(23,"V","Vanadium",50.942),
    Element(24,"Cr","Chromium",51.996),
    Element(25,"Mn","Manganese",54.938),
    Element(26,"Fe","Iron",55.845),
    Element(27,"Co","Cobalt",58.933),
    Element(28,"Ni","Nickel",58.693),
    Element(29,"Cu","Copper",63.546),
    Element(30,"Zn","Zinc",65.38),
    Element(31,"Ga","Gallium",69.723),
    Element(32,"Ge","Germanium",72.630),
    Element(33,"As","Arsenic",74.922),
    Element(34,"Se","Selenium",78.971),
    Element(35,"Br","Bromine",79.904),
    Element(36,"Kr","Krypton",83.798),
    Element(37,"Rb","Rubidium",85.468),
    Element(38,"Sr","Strontium",87.62),
    Element(39,"Y","Yttrium",88.906),
    Element(40,"Zr","Zirconium",91.224),
    Element(41,"Nb","Niobium",92.906),
    Element(42,"Mo","Molybdenum",95.95),
    Element(43,"Tc","Technetium",98.0),
    Element(44,"Ru","Ruthenium",101.07),
    Element(45,"Rh","Rhodium",102.91),
    Element(46,"Pd","Palladium",106.42),
    Element(47,"Ag","Silver",107.87),
    Element(48,"Cd","Cadmium",112.41),
    Element(49,"In","Indium",114.82),
    Element(50,"Sn","Tin",118.71),
    Element(51,"Sb","Antimony",121.76),
    Element(52,"Te","Tellurium",127.60),
    Element(53,"I","Iodine",126.90),
    Element(54,"Xe","Xenon",131.29),
    Element(55,"Cs","Cesium",132.91),
    Element(56,"Ba","Barium",137.33),
    Element(57,"La","Lanthanum",138.91),
    Element(58,"Ce","Cerium",140.12),
    Element(59,"Pr","Praseodymium",140.91),
    Element(60,"Nd","Neodymium",144.24),
    Element(61,"Pm","Promethium",145.0),
    Element(62,"Sm","Samarium",150.36),
    Element(63,"Eu","Europium",151.96),
    Element(64,"Gd","Gadolinium",157.25),
    Element(65,"Tb","Terbium",158.93),
    Element(66,"Dy","Dysprosium",162.50),
    Element(67,"Ho","Holmium",164.93),
    Element(68,"Er","Erbium",167.26),
    Element(69,"Tm","Thulium",168.93),
    Element(70,"Yb","Ytterbium",173.05),
    Element(71,"Lu","Lutetium",174.97),
    Element(72,"Hf","Hafnium",178.49),
    Element(73,"Ta","Tantalum",180.95),
    Element(74,"W","Tungsten",183.84),
    Element(75,"Re","Rhenium",186.21),
    Element(76,"Os","Osmium",190.23),
    Element(77,"Ir","Iridium",192.22),
    Element(78,"Pt","Platinum",195.08),
    Element(79,"Au","Gold",196.97),
    Element(80,"Hg","Mercury",200.59),
    Element(81,"Tl","Thallium",204.38),
    Element(82,"Pb","Lead",207.2),
    Element(83,"Bi","Bismuth",208.98),
    Element(84,"Po","Polonium",209.0),
    Element(85,"At","Astatine",210.0),
    Element(86,"Rn","Radon",222.0),
    Element(87,"Fr","Francium",223.0),
    Element(88,"Ra","Radium",226.0),
    Element(89,"Ac","Actinium",227.0),
    Element(90,"Th","Thorium",232.04),
    Element(91,"Pa","Protactinium",231.04),
    Element(92,"U","Uranium",238.03),
    Element(93,"Np","Neptunium",237.0),
    Element(94,"Pu","Plutonium",244.0),
    Element(95,"Am","Americium",243.0),
    Element(96,"Cm","Curium",247.0),
    Element(97,"Bk","Berkelium",247.0),
    Element(98,"Cf","Californium",251.0),
    Element(99,"Es","Einsteinium",252.0),
    Element(100,"Fm","Fermium",257.0),
    Element(101,"Md","Mendelevium",258.0),
    Element(102,"No","Nobelium",259.0),
    Element(103,"Lr","Lawrencium",266.0),
    Element(104,"Rf","Rutherfordium",267.0),
    Element(105,"Db","Dubnium",268.0),
    Element(106,"Sg","Seaborgium",269.0),
    Element(107,"Bh","Bohrium",270.0),
    Element(108,"Hs","Hassium",277.0),
    Element(109,"Mt","Meitnerium",278.0),
    Element(110,"Ds","Darmstadtium",281.0),
    Element(111,"Rg","Roentgenium",282.0),
    Element(112,"Cn","Copernicium",285.0),
    Element(113,"Nh","Nihonium",286.0),
    Element(114,"Fl","Flerovium",289.0),
    Element(115,"Mc","Moscovium",289.0),
    Element(116,"Lv","Livermorium",293.0),
    Element(117,"Ts","Tennessine",294.0),
    Element(118,"Og","Oganesson",294.0),
]

# Build lookup maps
BY_Z: Dict[int, Element] = {e.Z: e for e in ELEMENTS_LIST}
BY_SYMBOL: Dict[str, Element] = {e.symbol: e for e in ELEMENTS_LIST}
BY_NAME: Dict[str, Element] = {e.name.lower(): e for e in ELEMENTS_LIST}

def get_by_atomic_number(z: int) -> Element | None:
    return BY_Z.get(z)

def get_by_symbol(sym: str) -> Element | None:
    return BY_SYMBOL.get(sym.capitalize())

def get_by_name(name: str) -> Element | None:
    return BY_NAME.get(name.strip().lower())

# --- Chemical formula parsing and molar mass ---
TOKEN_RE = re.compile(r"""
    (?:\(|\)|·|\.|\+|-)         # parentheses / hydrate dot / +/- separators
  | ([A-Z][a-z]?)                   # element symbol
  | (\d+(?:\.\d+)?)              # number (integer or decimal)
""", re.VERBOSE)

def parse_formula(formula: str) -> Dict[str, float]:
    """Parse a chemical formula into a dict of element counts.
    Supports nested parentheses and hydrate dot (· or .).
    E.g., 'Ca(OH)2', 'CuSO4·5H2O', 'Fe2(SO4)3', 'KMnO4'
    Returns dict like {'Ca':1,'O':2,'H':2}
    """
    # Normalize hydrate separators to '+' (treated as addition of parts)
    f = formula.replace('·', '+').replace(' ', '')
    tokens = TOKEN_RE.findall(f)  # but our regex uses capturing groups; handle differently
    # Because of capturing groups, findall returns tuples; we need a different approach:
    tokens = []
    i = 0
    while i < len(f):
        ch = f[i]
        if ch in '().+-':
            tokens.append(ch)
            i += 1
            continue
        if ch == '·':
            tokens.append('+'); i += 1; continue
        if ch.isupper():
            j = i+1
            while j < len(f) and f[j].islower():
                j += 1
            tokens.append(f[i:j])  # symbol
            i = j
            continue
        if ch.isdigit():
            j = i+1
            dot_seen = False
            while j < len(f) and (f[j].isdigit() or (f[j]=='.' and not dot_seen)):
                if f[j]=='.':
                    dot_seen = True
                j += 1
            tokens.append(f[i:j])  # number (may be decimal multiplier)
            i = j
            continue
        raise ValueError(f"Unexpected character '{ch}' in formula.")
    # Shunting-yard style parse with multiplier stack
    def merge(counts: Dict[str,float], sym: str, n: float):
        counts[sym] = counts.get(sym, 0.0) + n
    def multiply(block: Dict[str,float], factor: float) -> Dict[str,float]:
        return {k: v*factor for k, v in block.items()}

    # We'll split by '+' (hydrates / additions), parse each chunk, then sum
    def parse_chunk(chunk_tokens: List[str]) -> Dict[str,float]:
        stack: List[Dict[str,float]] = []
        counts: Dict[str,float] = {}
        i = 0
        while i < len(chunk_tokens):
            tok = chunk_tokens[i]
            if tok == '(':
                # find matching ')'
                depth = 1
                j = i+1
                while j < len(chunk_tokens):
                    if chunk_tokens[j] == '(':
                        depth += 1
                    elif chunk_tokens[j] == ')':
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                if depth != 0:
                    raise ValueError("Unbalanced parentheses in formula.")
                inner = parse_chunk(chunk_tokens[i+1:j])
                # possible multiplier after ')'
                k = j+1
                mult = 1.0
                if k < len(chunk_tokens) and re.fullmatch(r"\d+(?:\.\d+)?", chunk_tokens[k] or ''):
                    mult = float(chunk_tokens[k])
                    i = k  # will be incremented below
                else:
                    i = j
                # merge multiplied inner
                for s, n in inner.items():
                    merge(counts, s, n*mult)
            elif tok == ')':
                # should not happen here
                raise ValueError("Unbalanced ')'")
            elif re.fullmatch(r"[A-Z][a-z]?", tok):
                # element possibly followed by a number
                mult = 1.0
                if i+1 < len(chunk_tokens) and re.fullmatch(r"\d+(?:\.\d+)?", chunk_tokens[i+1] or ''):
                    mult = float(chunk_tokens[i+1])
                    i += 1
                merge(counts, tok, mult)
            elif re.fullmatch(r"\d+(?:\.\d+)?", tok):
                # stand-alone leading multiplier like '5H2O' at start: apply to following group or element
                # We'll treat it as multiplying the rest of the chunk parsed recursively.
                # Implement by parsing the remainder and then scaling.
                mult = float(tok)
                rest = parse_chunk(chunk_tokens[i+1:])
                for s, n in rest.items():
                    merge(counts, s, n*mult)
                return counts
            else:
                # ignore '+' here; should be split earlier
                pass
            i += 1
        return counts

    # split by '+'
    parts: List[List[str]] = []
    start = 0
    for idx, tok in enumerate(tokens):
        if tok == '+' or tok == '-':  # '-' also separator sometimes in adduct names
            parts.append(tokens[start:idx])
            start = idx+1
    parts.append(tokens[start:])
    total: Dict[str,float] = {}
    for part in parts:
        sub = parse_chunk(part)
        for s, n in sub.items():
            total[s] = total.get(s, 0.0) + n
    return total

def molar_mass(formula: str) -> float:
    counts = parse_formula(formula)
    mass = 0.0
    missing: List[str] = []
    for sym, n in counts.items():
        el = get_by_symbol(sym)
        if not el:
            missing.append(sym)
            continue
        mass += el.atomic_mass * n
    if missing:
        raise KeyError(f"Unknown element symbols in formula: {', '.join(missing)}")
    return mass

def pretty_counts(counts: Dict[str,float]) -> str:
    parts = []
    for sym in sorted(counts.keys(), key=lambda s: BY_SYMBOL[s].Z if s in BY_SYMBOL else 999):
        n = counts[sym]
        if abs(n - round(n)) < 1e-9:
            n_str = '' if int(round(n)) == 1 else str(int(round(n)))
        else:
            n_str = str(n)
        parts.append(f"{sym}{n_str}")
    return ''.join(parts)

def print_table():
    print("\nPeriodic Table (Z, Symbol, Name, Atomic Mass)\n" + '-'*52)
    for e in ELEMENTS_LIST:
        print(f"{e.Z:3d}  {e.symbol:<3}  {e.name:<14}  {e.atomic_mass:7.3f}")

def print_element(e: Element):
    print(f"\nAtomic Number : {e.Z}\nSymbol        : {e.symbol}\nName          : {e.name}\nAtomic Mass   : {e.atomic_mass} g/mol")

def quiz_mode():
    """Start quiz mode with random periodic table questions."""
    print("\n--- QUIZ MODE ---")
    print("Answer the questions. Type 'exit' to stop quiz.\n")

    score = 0
    total = 0

    QUESTIONS = [
        "symbol_from_number",
        "number_from_symbol",
        "name_from_symbol",
        "symbol_from_name",
        "mass_from_symbol"
    ]

    while True:
        qtype = random.choice(QUESTIONS)
        element = random.choice(ELEMENTS_LIST)
        total += 1

        if qtype == "symbol_from_number":
            ans = input(f"Q{total}: What is the symbol of element with atomic number {element.Z}? ")
            if ans.strip().capitalize() == element.symbol:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Wrong. Correct answer: {element.symbol}")

        elif qtype == "number_from_symbol":
            ans = input(f"Q{total}: What is the atomic number of {element.symbol}? ")
            if ans.strip().isdigit() and int(ans) == element.Z:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Wrong. Correct answer: {element.Z}")

        elif qtype == "name_from_symbol":
            ans = input(f"Q{total}: What is the name of element {element.symbol}? ")
            if ans.strip().lower() == element.name.lower():
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Wrong. Correct answer: {element.name}")

        elif qtype == "symbol_from_name":
            ans = input(f"Q{total}: What is the symbol of {element.name}? ")
            if ans.strip().capitalize() == element.symbol:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Wrong. Correct answer: {element.symbol}")

        elif qtype == "mass_from_symbol":
            ans = input(f"Q{total}: Approximate atomic mass of {element.symbol}? (g/mol) ")
            try:
                if abs(float(ans) - element.atomic_mass) < 0.5:  # small tolerance
                    print("✅ Correct (within tolerance)!")
                    score += 1
                else:
                    print(f"❌ Wrong. Correct answer: {element.atomic_mass}")
            except ValueError:
                print(f"❌ Wrong. Correct answer: {element.atomic_mass}")

        # Exit condition
        if ans.strip().lower() == "exit":
            total -= 1  # don't count the exit as a question
            break

        print(f"Score: {score}/{total}\n")

    print(f"Final Score: {score}/{total}")
    print("Exiting Quiz Mode...\n")

# -------------------------
# Equation Balancer
# -------------------------
def balance_equation(equation: str) -> str:
    try:
        left, right = equation.split("->")
        reactants = [x.strip() for x in left.split("+")]
        products = [x.strip() for x in right.split("+")]
        species = reactants + products

        # Parse formulas
        all_elements = set()
        parsed = []
        for spc in species:
            counts = parse_formula(spc)
            parsed.append(counts)
            all_elements.update(counts.keys())

        all_elements = sorted(all_elements)
        n = len(species)

        # Build matrix
        matrix = []
        for elem in all_elements:
            row = []
            for j, counts in enumerate(parsed):
                cnt = counts.get(elem, 0)
                if j < len(reactants):
                    row.append(cnt)
                else:
                    row.append(-cnt)
            matrix.append(row)

        M = sp.Matrix(matrix)
        nullspace = M.nullspace()
        if not nullspace:
            return "No solution found."

        coeffs = nullspace[0]
        lcm = sp.lcm([term.q for term in coeffs])
        coeffs = [int(term * lcm) for term in coeffs]

        # Format equation
        left_side = " + ".join(f"{coeffs[i]} {reactants[i]}" for i in range(len(reactants)))
        right_side = " + ".join(f"{coeffs[i+len(reactants)]} {products[i]}" for i in range(len(products)))
        return left_side + " -> " + right_side
    except Exception as e:
        return f"Error: {e}"

# -------------------------
        #Main Menu 
# -------------------------
def main():
    while True:
        print("\n--- Periodic Table CLI ---")
        print("1. Find element by atomic number")
        print("2. Find element by symbol")
        print("3. Find element by name")
        print("4. Calculate molar mass")
        print("5. Quiz mode")
        print("6. Balance chemical equation")
        print("7. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            try:
                Z = int(input("Enter atomic number: "))
                el = get_by_atomic_number(Z)
                if el:
                    print(el)
                else:
                    print("Not found.")
            except ValueError:
                print("Invalid input.")

        elif choice == "2":
            sym = input("Enter symbol: ")
            el = get_by_symbol(sym)
            if el:
                print(el)
            else:
                print("Not found.")

        elif choice == "3":
            name = input("Enter name: ")
            el = get_by_name(name)
            if el:
                print(el)
            else:
                print("Not found.")

        elif choice == "4":
            formula = input("Enter chemical formula (e.g., H2O, Ca(OH)2, CuSO4·5H2O): ")
            try:
                counts = parse_formula(formula)
                mass = molar_mass(counts)
                print("Composition:", pretty_counts(counts))
                print(f"Molar mass = {mass:.3f} g/mol")
            except Exception as e:
                print("Error:", e)

        elif choice == "5":
            quiz_mode()

        elif choice == "6":
             eq = input("Enter chemical equation (e.g., H2 + O2 -> H2O): ")
             print("Balanced:", balance_equation(eq))


        elif choice == "7":
            print("Goodbye!")
            break  
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    main()


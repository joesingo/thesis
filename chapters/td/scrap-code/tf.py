from truthdiscovery import Dataset, TruthFinder, FixedIterator

t0 = 0.9
gamma = 0.3
rho = 0.5
lam = 0
max_its = 100


tuples = [
    ("s", "o1", 1),
    ("s", "o2", 1),
    ("t", "o1", 2),
    ("t", "o2", 2),
    ("u", "o2", 2),
    ("v", "o2", 2),
]


def imp(var, val1, val2):
    # Implication is close to 1 when val1, val2 are close, and goes to -1
    # when they are far apart.
    #
    # Note that this example does not consider the value of `var`. In
    # principle the calculation for implication can differ between
    # variables.
    return -lam if val1 != val2 else 0


mydata = Dataset(tuples, implication_function=imp)
it = FixedIterator(limit=max_its)
alg = TruthFinder(influence_param=rho, dampening_factor=gamma,
                  initial_trust=t0, iterator=it)
res = alg.run(mydata)

print("from td library:")
print(res.trust)
print(res.belief)

src = {
    "c": {"s"},
    "d": {"t"},
    "e": {"s"},
    "f": {"t", "u", "v"},
}
antisrc = {
    "c": {"t"},
    "d": {"s"},
    "e": {"t", "u", "v"},
    "f": {"s"},
}
claim = {
    "s": {"c", "e"},
    "t": {"d", "f"},
    "u": {"f"},
    "v": {"f"},
}

sources = {"s", "t", "u", "v"}
claims = {"c", "d", "e", "f"}

scores = {x: t0 for x in set.union(sources, claims)}

for its in range(max_its):
    for c in claims:
        q = 1
        for s in src[c]:
            q *= (1 - scores[s]) ** (gamma)
        for t in antisrc[c]:
            q /= (1 - scores[t]) ** (gamma * rho * lam)
        scores[c] = 1 / (1 + q)

    for s in sources:
        q = 0
        for c in claim[s]:
            q += scores[c]
        scores[s] = q / len(claim[s])

for x in scores:
    scores[x] = f"{scores[x]:.4f}"

print("from handcrafted code:")
print(scores)

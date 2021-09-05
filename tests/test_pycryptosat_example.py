import pycryptosat as SAT


def test_sat_smoke():
    solver = SAT.Solver()
    solver.add_clauses([[1,2], [2], [-1], [3,4,5,6]])
    solver.add_xor_clause([1,3,6], True)  # x₁ ⊕ x₃ ⊕ x₆ = 1

    is_sat, model = solver.solve()

    assert is_sat

    # First element is padding so that indicies match. 
    assert len(model) - 1 == 6

    # Normal CNF constraints.
    assert model[1] or model[2]  # [1, 2]
    assert model[2]              # [2]
    assert not model[1]          # [-1]
    assert any(model[3:7])       # [3,4,5,6]

    # XOR constraint.
    assert model[1] ^ model[3] ^ model[6]


def test_unsat_smoke():
    solver = SAT.Solver()
    solver.add_clauses([[1,2], [2], [-1]])
    solver.add_xor_clause([1,2], False)  # x₁ ⊕ x₂ = 0

    is_sat, model = solver.solve()
    assert not is_sat
    assert model is None

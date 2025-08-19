# TODO replace "START" -> X with Init{X} constraint
# TODO transitive closure for loops of length 2




import pytest
import pandas as pd
from refactored import (
    build_mirrored_matrix,
    parse_relation_matrix,
    compute_transitive_closure,
    generate_binary_constraints,
    ChainResponse,
    AlternateResponse,
)

def run_full_pipeline(df):
    """Takes a DataFrame and returns the final set of constraints."""
    d, e_matrix = parse_relation_matrix(df)
    e_tc = compute_transitive_closure(d)
    final_e = e_matrix.union(e_tc)
    constraints = generate_binary_constraints(d, final_e)
    return constraints


def test_pattern_exclusive_choice():
    """Tests an exclusive choice: Start -> A -> {B XOR C} -> D."""
    activities = ['A', 'B', 'C', 'D']
    start_activities = ['A']
    primary_relations = [('A', 'B', '→'), ('A', 'C', '→'), ('B', 'D', '→'), ('C', 'D', '→')]
    df = build_mirrored_matrix(activities, start_activities, primary_relations)
    
    expected_constraints = {
        ChainResponse(frozenset({'Start'}), frozenset({'A'})),
        ChainResponse(frozenset({'A'}), frozenset({'B', 'C'})),
        ChainResponse(frozenset({'B'}), frozenset({'D'})),
        ChainResponse(frozenset({'C'}), frozenset({'D'})),
        # TC finds Start -> {B, C, D} and A -> D
        AlternateResponse(frozenset({'Start'}), frozenset({'B', 'C', 'D'})),
        AlternateResponse(frozenset({'A'}), frozenset({'D'}))
    }
    assert run_full_pipeline(df) == expected_constraints

def test_pattern_parallelism_without_bypass():
    """Tests a parallel flow: Start -> A -> (B || C) -> D."""
    activities = ['A', 'B', 'C', 'D']
    start_activities = ['A']
    primary_relations = [('A', 'B', '→'), ('A', 'C', '→'), ('B', 'C', '||'), ('B', 'D', '→'), ('C', 'D', '→')]
    df = build_mirrored_matrix(activities, start_activities, primary_relations)
    
    expected_constraints = {
        ChainResponse(frozenset({'Start'}), frozenset({'A'})),
        ChainResponse(frozenset({'A'}), frozenset({'B', 'C'})),
        ChainResponse(frozenset({'B'}), frozenset({'C', 'D'})),
        ChainResponse(frozenset({'C'}), frozenset({'B', 'D'})),
        # B and C are NOT optional from A because the bypass A->D is not in D.
        AlternateResponse(frozenset({'A'}), frozenset({'B'})),
        AlternateResponse(frozenset({'A'}), frozenset({'C'})),
        # TC finds Start -> {B,C,D} and A -> D
        AlternateResponse(frozenset({'Start'}), frozenset({'B', 'C', 'D'})),
        AlternateResponse(frozenset({'A'}), frozenset({'D'}))
    }
    assert run_full_pipeline(df) == expected_constraints
    
def test_pattern_parallelism_with_bypass():
    """Tests a parallel flow with bypass: Start -> A -> (B || C) -> D, plus A -> D."""
    activities = ['A', 'B', 'C', 'D']
    start_activities = ['A']
    primary_relations = [('A', 'B', '→'), ('A', 'C', '→'), ('A', 'D', '→'), ('B', 'C', '||'), ('B', 'D', '→'), ('C', 'D', '→')]
    df = build_mirrored_matrix(activities, start_activities, primary_relations)
    
    expected_constraints = {
        ChainResponse(frozenset({'Start'}), frozenset({'A'})),
        ChainResponse(frozenset({'A'}), frozenset({'B', 'C', 'D'})),
        ChainResponse(frozenset({'B'}), frozenset({'C', 'D'})),
        ChainResponse(frozenset({'C'}), frozenset({'B', 'D'})),
        
        AlternateResponse(frozenset({'Start'}), frozenset({'B', 'C', 'D'}))
    }
    assert run_full_pipeline(df) == expected_constraints

def test_pattern_structured_loop():
    """Tests a structured loop: Start -> A -> B -> C -> B ... -> D."""
    activities = ['A', 'B', 'C', 'D']
    start_activities = ['A']
    primary_relations = [('A', 'B', '→'), ('B', 'C', '||'), ('C', 'D', '→')]
    df = build_mirrored_matrix(activities, start_activities, primary_relations)
    
    expected_constraints = {
        ChainResponse(frozenset({'Start'}), frozenset({'A'})),
        ChainResponse(frozenset({'A'}), frozenset({'B'})),
        ChainResponse(frozenset({'B'}), frozenset({'C'})),
        ChainResponse(frozenset({'C'}), frozenset({'B', 'D'})),

        AlternateResponse(frozenset({'Start'}), frozenset({'B', 'C', 'D'})),
        AlternateResponse(frozenset({'A'}), frozenset({'C', 'D'})),
        AlternateResponse(frozenset({'B'}), frozenset({'D'}))
    }
    assert run_full_pipeline(df) == expected_constraints

def test_pattern_multiple_start_activities():
    """Tests a process that can start with either A or B."""
    activities = ['A', 'B', 'C']
    start_activities = ['A', 'B'] # Multiple entry points
    primary_relations = [('A', 'C', '→'), ('B', 'C', '→')]
    df = build_mirrored_matrix(activities, start_activities, primary_relations)

    expected_constraints = {
        # Start can be followed by A or B
        ChainResponse(frozenset({'Start'}), frozenset({'A', 'B'})),
        ChainResponse(frozenset({'A'}), frozenset({'C'})),
        ChainResponse(frozenset({'B'}), frozenset({'C'})),
        
        AlternateResponse(frozenset({'Start'}), frozenset({'C'}))
    }
    assert run_full_pipeline(df) == expected_constraints
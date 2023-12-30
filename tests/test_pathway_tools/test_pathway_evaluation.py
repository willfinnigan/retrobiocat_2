from rbc2.configs.source_mol_config import SourceMol_Config
from rbc2.pathway_tools.pathway_evaluation import leaf_molecule_availability, cost_pathway, rank_pathways
from rbc2.reaction_evaluation.starting_material_evaluator.starting_material_evaluator import \
    DefaultSQLStartingMaterialEvaluator
from rbc2.reaction_network_entities.pathway import Pathway
from rbc2.reaction_network_entities.reaction import Reaction


def test_pathway_with_only_target_returns_target_as_leaf():
    pathway = Pathway([], target_smi='CCCC=O')

    source_mol_config = SourceMol_Config()
    sme = DefaultSQLStartingMaterialEvaluator(config=source_mol_config)
    available, not_available = leaf_molecule_availability(pathway, sme)
    assert not_available == ['CCCC=O']

def test_pathway_costing():
    reaction1 = Reaction('CCCC=O', ['CCCCO', 'C=O'])
    reaction2 = Reaction('CCCCO', ['CCCCN'])
    pathway = Pathway([reaction1, reaction2])

    cost = cost_pathway(pathway, DefaultSQLStartingMaterialEvaluator())
    assert cost == 5.0625

def test_rank_pathways():
    reaction1 = Reaction('CCCC=O', ['CCCCO', 'C=O'])
    pathway1 = Pathway([reaction1])

    reaction2 = Reaction('CCCCO', ['CCCCN'])
    pathway2 = Pathway([reaction2])

    reaction3 = Reaction('CCCCN', ['CCCC=O'])
    pathway3 = Pathway([reaction3])

    pathways = [pathway1, pathway2, pathway3]
    scores = [10, 1, 5]

    ranked_pathways = rank_pathways(pathways, scores)
    assert ranked_pathways[0] == pathway2
    assert ranked_pathways[1] == pathway3
    assert ranked_pathways[2] == pathway1
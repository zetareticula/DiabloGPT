import numpy as np
import logging
from mumfordswitch.code_generation.convert_conditions import convert_range
from mumfordswitch.structure.base import Sum
from mumfordswitch.algorithms.inference import likelihood
from mumfordswitch.structure.base import Product
from FACE.algorithms.Inference import likelihood
from mumfordswitch.structure.base import Node
import os
import sys
from mumfordswitch.code_generation.convert_conditions import convert_range
from mumfordswitch.structure.base import Sum
from mumfordswitch.algorithms.inference import likelihood
from mumfordswitch.structure.base import Product
from FACE.algorithms.Inference import likelihood
from mumfordswitch.structure.base import Node



class MetaType:
    """
    This class represents the meta type of the attribute.
    """
    def __init__(self, meta_type):
        self.meta_type = meta_type

    def get_meta_type(self):
        return self.meta_type
    
class Evidence:
    """
    This class represents the evidence for the expectation computation.
    """
    def __init__(self, ranges):
        self.ranges = ranges

    def get_evidence_scope(self):
        return set([i for i, r in enumerate(self.ranges[0]) if r is not None])

    def get_evidence(self):
        return self.ranges
    
class ExpectationResult:
    """
    This class represents the result of the expectation computation.
    """
    def __init__(self, result):
        self.result = result

    def get_result(self):
        return self.result
    
    

# Add the parent directory to the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import the necessary packages and modules

logger = logging.getLogger(__name__)


class Range:
    """
    This is the base class for all range classes.
    """
    def __init__(self, null_value=None, is_not_null_condition=False):
        self.is_not_null_condition = is_not_null_condition
        self.null_value = null_value

    def is_impossible(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def get_ranges(self):
        raise NotImplementedError("Subclasses must implement this method.")

class NominalRange(Range):
    """
    This class specifies the range for a nominal attribute. It contains a list of integers which
    represent the values which are in the range.

    e.g. possible_values = [5,2]
    """
    def __init__(self, possible_values, null_value=None, is_not_null_condition=False):
        super().__init__(null_value, is_not_null_condition)
        self.possible_values = np.array(possible_values, dtype=np.int64)

    def is_impossible(self):
        return len(self.possible_values) == 0

    def get_ranges(self):
        return self.possible_values

class NumericRange(Range):
    """
    This class specifies the range for a numeric attribute. It contains a list of intervals which
    represents the values which are valid. Inclusive Intervals specifies whether upper and lower bound are included.

    e.g. ranges = [[10,15],[22,23]] if valid values are between 10 and 15 plus 22 and 23 (bounds inclusive)
    """
    def __init__(self, ranges, inclusive_intervals=None, null_value=None, is_not_null_condition=False):
        super().__init__(null_value, is_not_null_condition)
        self.ranges = ranges
        self.inclusive_intervals = inclusive_intervals
        if self.inclusive_intervals is None:
            self.inclusive_intervals = []
            for interval in self.ranges:
                self.inclusive_intervals.append([True, True])

    def is_impossible(self):
        return len(self.ranges) == 0

    def get_ranges(self):
        return self.ranges

class Evidence:
    """
    This class represents the evidence for the expectation computation.
    """
    def __init__(self, ranges):
        self.ranges = ranges

    def get_evidence_scope(self):
        return set([i for i, r in enumerate(self.ranges[0]) if r is not None])

    def get_evidence(self):
        return self.ranges

def expectation(FACE, feature_scope, inverted_features, evidence, node_expectation=None, node_likelihoods=None,
                use_generated_code=False, spn_id=None, meta_types=None, gen_code_stats=None):
    """Compute the Expectation:
        E[1_{conditions} * X_feature_scope]
        First factor is one if condition is fulfilled. For the second factor the variables in feature scope are
        multiplied. If inverted_features[i] is True, variable is taken to denominator.
        The conditional expectation would be E[1_{conditions} * X_feature_scope]/P(conditions)
    """
    evidence_scope = evidence.get_evidence_scope()
    assert not (len(evidence_scope) > 0 and evidence.get_evidence() is None)
    # Perform the computation for expectation here
    return expectation_result

class ExpectationResult:
    """
    This class represents the result of the expectation computation.
    """
    def __init__(self, result):
        self.result = result

    def get_result(self):
        return self.result

def expectation(FACE, feature_scope, inverted_features, ranges, node_expectation=None, node_likelihoods=None,
                use_generated_code=False, spn_id=None, meta_types=None, gen_code_stats=None):
    """Compute the Expectation:
        E[1_{conditions} * X_feature_scope]
        First factor is one if condition is fulfilled. For the second factor the variables in feature scope are
        multiplied. If inverted_features[i] is True, variable is taken to denominator.
        The conditional expectation would be E[1_{conditions} * X_feature_scope]/P(conditions)
    """

    # evidence_scope = set([i for i, r in enumerate(ranges) if not NP.isnan(r)])
    global parameters

    evidence_scope = set([i for i, r in enumerate(ranges[0]) if r is not None])
    evidence = ranges

    assert not (len(evidence_scope) > 0 and evidence is None)
    # we need to check if the evidence is not None
    relevant_scope = set()
    relevant_scope.update(evidence_scope)

    # Perform the computation for expectation here

    return expectation_result




class NominalRange:
    """
    This class specifies the range for a nominal attribute. It contains a list of integers which
    represent the values which are in the range.
    
    e.g. possible_values = [5,2] 
    """

    def __init__(self, possible_values, null_value=None, is_not_null_condition=False):
        self.is_not_null_condition = is_not_null_condition
        self.possible_values = np.array(possible_values, dtype=np.int64)
        self.null_value = null_value

    def is_impossible(self):
        return len(self.possible_values) == 0

    def get_ranges(self):
        return self.possible_values


class NumericRange:
    """
    This class specifies the range for a numeric attribute. It contains a list of intervals which
    represents the values which are valid. Inclusive Intervals specifies whether upper and lower bound are included.
    
    e.g. ranges = [[10,15],[22,23]] if valid values are between 10 and 15 plus 22 and 23 (bounds inclusive)
    """

    def __init__(self, ranges, inclusive_intervals=None, null_value=None, is_not_null_condition=False):
        self.is_not_null_condition = is_not_null_condition
        self.ranges = ranges
        self.null_value = null_value
        self.inclusive_intervals = inclusive_intervals
        if self.inclusive_intervals is None:
            self.inclusive_intervals = []
            for interval in self.ranges:
                self.inclusive_intervals.append([True, True])

    def is_impossible(self):
        return len(self.ranges) == 0

    def get_ranges(self):
        return self.ranges

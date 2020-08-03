from typing import List, Dict, Callable, Tuple
SlotValidationResult = Tuple[bool, bool, str, Dict]

def validate_finite_values_entity(values: List[Dict], supported_values: List[str] = None,
                                invalid_trigger: str = None, key: str = None,
                                support_multiple: bool = True, pick_first: bool = False, **kwargs) -> SlotValidationResult:
    """
    Validate an entity on the basis of its value extracted.
    The method will check if the values extracted("values" arg) lies within the finite list of supported values(arg "supported_values").

    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param supported_values: List of supported values for the slot
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :return: a tuple of (filled, partially_filled, trigger, params)
    """

    if support_multiple == False and pick_first == False:
        return (False, False, "", {})
    
    if len(values) == 0:
        return (False, False, invalid_trigger, {})

    valid_values = []
    for value in values:
        if value["value"] in supported_values:
            valid_values.append(value["value"].upper())

    return validate_entity_helper(valid_values, len(values), pick_first, key, invalid_trigger)


def validate_numeric_entity(values: List[Dict], invalid_trigger: str = None, key: str = None,
                            support_multiple: bool = True, pick_first: bool = False, constraint=None, var_name=None,
                            **kwargs) -> SlotValidationResult:
    """
    Validate an entity on the basis of its value extracted.
    The method will check if that value satisfies the numeric constraints put on it.
    If there are no numeric constraints, it will simply assume the value is valid.

    If there are numeric constraints, then it will only consider a value valid if it satisfies the numeric constraints.
    In case of multiple values being extracted and the support_multiple flag being set to true, the extracted values
    will be filtered so that only those values are used to fill the slot which satisfy the numeric constraint.

    If multiple values are supported and even 1 value does not satisfy the numeric constraint, the slot is assumed to be
    partially filled.

    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :param constraint: Conditional expression for constraints on the numeric values extracted
    :param var_name: Name of the var used to express the numeric constraint
    :return: a tuple of (filled, partially_filled, trigger, params)
    """  

    if support_multiple == False and pick_first == False:
        return (False, False, "", {})

    if len(values) == 0:
        return (False, False, invalid_trigger, {})

    valid_values = []
    expression = compile(constraint, "<string>", "eval")
    for value in values:
        if eval(expression, {var_name: value["value"]}):
            valid_values.append(value["value"])
    
    return validate_entity_helper(valid_values, len(values), pick_first, key, invalid_trigger)


def validate_entity_helper(valid_values: List[str],num_total_values: int, pick_first: bool, key: str,
                        invalid_trigger: str) -> SlotValidationResult:

    """
    Contains the common logic of creating the SlotValidationResult for validate_finite_values_entity and validate_numeric_entity functions
    
    :param valid_values: A list of all the valid values
    :param num_total_values: Number of total values (valid + invalid)
    :param pick_first: Set to true if the first value is to be picked up
    :param key: Dict key to use in the params returned
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :return: a tuple of (filled, partially_filled, trigger, params)
    """

    if len(valid_values) == num_total_values:
        filled, partially_filled, trigger = True, False, ""
        if pick_first:
            params = {key: valid_values[0]} 
        else:
            params = {key: valid_values}
    else:
        filled, partially_filled, trigger  = False, True, invalid_trigger
        if len(valid_values) > 0 and pick_first:
            params = {key: valid_values[0]} 
        else:
            params = {}

    return (filled, partially_filled, trigger, params)
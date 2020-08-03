from typing import List, Dict, Callable, Tuple
SlotValidationResult = Tuple[bool, bool, str, Dict]

def validate_finite_values_entity(values: List[Dict], supported_values: List[str] = None,
                                invalid_trigger: str = None, key: str = None,
                                support_multiple: bool = True, pick_first: bool = False, **kwargs) -> SlotValidationResult:
    
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
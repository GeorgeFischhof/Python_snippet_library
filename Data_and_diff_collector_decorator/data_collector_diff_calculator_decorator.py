
from functools import wraps


def collect_data_and_calculate_difference(data_collector, difference_calculator):
    """Returns difference of data collected before and after the decorated function, 
    plus the original return value of the decorated function. Return type: dict.
    Keys: 
        - function names of the decorated function
        - name of the difference calculator function
    Values: 
        - difference calculated by difference_calculator function 
        - the original return value for decorated function
    Parameters: functions to collect data, and create difference from collected data
    """

    def function_wrapper_because_of_parameters(decorated_function):
        difference_calculator_name = difference_calculator.__name__
        decorated_function_name = decorated_function.__name__

        i_am_the_first_decorator = not hasattr(decorated_function, '__wrapped__')

        @wraps(decorated_function)
        def wrapper(*args, **kwargs) -> dict:
            result_dict = dict()

            before = data_collector()
            original_result = decorated_function(*args, **kwargs)
            after = data_collector()

            my_collection = difference_calculator(before=before, after=after)

            i_am_not_first_decorator_but_first_is_similar_to_me = (
                not i_am_the_first_decorator
                and isinstance(original_result, dict)
                and (decorated_function_name in original_result)
            )

            if i_am_not_first_decorator_but_first_is_similar_to_me:
                original_result[difference_calculator_name] = my_collection
                return original_result
            else:
                result_dict[decorated_function_name] = original_result
                result_dict[difference_calculator_name] = my_collection
                return result_dict

        return wrapper
    return function_wrapper_because_of_parameters


# Usage

"""
@collect_data_and_calculate_difference(
    data_collector=collect_tracking_data_parameters,
    difference_calculator=calculate_tracking_data_difference)
@collect_data_and_calculate_difference(
    data_collector=collect_device_accounting_parameters,
    difference_calculator=calculate_device_accounting_difference)
def check_printing():
    return 'printing result...'


print(check_printing())

"""

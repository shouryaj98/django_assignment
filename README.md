# Assignment

### Steps to run the project:

1. Clone the repository locally.
2. Change directory to the root directory of the project and build the image using `docker build -t django-app .` command. 
3. Run the Django app using `docker container run --name web-app --network=host django-app` command.

### Docker image size = 119 MB

### Assumptions:

1. `entity_type` key (in `values` array) always has a valid value.
2. `values` list does not contain duplicates.
3. Each of the object/dict in the `values` array has the `value` key in it.

4.  | `support_multiple` | `pick_first` |                                                                                                                                                      |
    |------------------|------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
    | false            | false      | Output is always (False, False, "", {})                                                                                                              |
    | false            | true       | `ids_stated` in params must be a string instead of a list.                                                                                             |
    | true             | false      | `ids_stated` must be a list of supported IDs passed in the values list. If all the values are invalid, params = {} (Concluded from 1st POST API examples)                                                                             |
    | true             | true       | `ids_stated` in params must be a string instead of a list. `pick_first` is given priority over `support_multiple`. (Concluded from 2nd POST API examples)  |

5. `name`, `reuse`, `validation_parser` and `type` are not required for the given problem statement.

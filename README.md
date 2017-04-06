# django_utils
Django utility functions and libraries that I have written over time and regularly use. All the libraries/functions are inside the `common` directory.

Details about the libraries included to help you get started.

#### `common.external`
External libraries that I use in my django projects.
* `common.external.showme` -- This is an external package that I use for profiling function times. The most useful decorator of this library is `showme.time`

#### `common.logging`
Use this package to add logging to your django rest framework ViewSets. Following are the steps required for using this package:
* Add `common.logging.middleware.LoggingMiddleware` to the django setting `MIDDLEWARE_CLASSES`.
* Configure the logging setting in django settings. You can refer `django_utils.settings.LOGGING` for this purpose
* Use the mixin `common.logging.mixins.APILoggingMixin` in your ViewSets

#### `common.utils`
Set of utility functions/libraries that can be imported into any python app.
* #### `utils.admin_filters`
  Filters that can be imported into any django admin to give additional support.
  Currently, the `IsNullBlank` filter is available, which adds an additional set of django admin filters with options as
  `Has Value`, `None` (for fields with `null=True`), `Blank` (fields with `blank=True`) & `Null or Blank` (fields with both `null=True, blank=True`). Inherit this filter to create custom filter as follows:
  ```python
  from common.utils.admin_filters import IsNullBlankFilter
  class PostTitleFilter(IsNullBlankFilter):
      title = 'Post Title'
      parameter_name = 'title'
      show_blank_filter = True
      show_null_filter = False
  ```
* #### `utils.date_ops`
  Set of functions for retrieving/constructing date time objects and time ranges. Refer the function documentation for details. Usage as follows:
  ```python
  from common.utils.date_ops import DateTimeOperations as DtOps
  print(DtOps.ist_datetime(2017, 4, 14))
  print(DtOps.ist_now())
  print(DtOps.get_range_calendar_year())
  ```
* #### `utils.exception`
  Use `ExceptionLogger` for detailed logging of exceptions inside your code. Usage as follows:
  ```python
  from common.utils.exception import ExceptionLogger
  try:
      # do something
      raise Exception
  except:
      ExceptionLogger.print_exception()
  ```
* #### `utils.file_ops`
  Set of functions to delete files and create/remove/recreate directories. Usage is self-explanatory.
* #### `utils.http`
  Primarily used for creating django responses with downloadable file objects.
* #### `utils.logged_requests`
  Python's `requests` library enhanced with extensive logging. This library contains two sets of functions as follows:
  * `LoggedRequests` -- wrapper over the vanilla requests methods. Usage as follows:
    ```python
    from common.utils.logged_requests import LoggedRequests
    LoggedRequests.get('http://icanhazip.com', log_title='Demo for LoggedRequests ')
    ```
  * `PatchedRequests` -- monkey patches the vanilla requests functions with logging details. The effect of using this is entire project wide. Usage as follows:
    ```python
    # inside __init__.py
    from common.utils.logged_requests import PatchedRequests
    PatchedRequests.patch_library()

    # For sending requests in any other file use the vanilla request library as is with additional parameters log_title & log_response_data
    import requests
    requests.get('http://icanhazip.com', log_title='Demo for LoggedRequests ') # Gives the same result as LoggedRequests.get
    ```
* #### `utils.model_fields`
  Custom fields used across django models:
  * `DefaultTZDateTimeField` -- A wrapper over `models.DateTimeField` that converts db value of datetime fields to django setting's timezone.
  * `CurrencyField` -- A wraper over `models.FloatField` that saves and retrieves numbers as 2-decimal precision values for monetary calculations.
* #### `utils.models`
  Contains `MetaDataModel` which has the basic meta data fields that ideally every model object should have.
* #### `utils.queryset`
  Contains `QuerysetHelpers`, a set of functions to help create querysets dynamically.
* #### `utils.s3`
  Set of functions to access amazon s3 buckets & push/pull objects to/from the same.
* #### `utils.validators`
  Set of functions that I use across my projects for variable validations.
* #### `utils.vars`
  Set of variables that I use for my personal semantic understandings.

Feel free to use/modify/share the libraries & functions as per your discretion. Happy Coding.

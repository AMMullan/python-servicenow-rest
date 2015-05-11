# python-servicenow-rest

The REST API is active by default in all instances, starting with the Eureka release.

Compatible with both Python 2 and 3. Tested with 2.7 and 3.4.

For more info, see:

http://wiki.servicenow.com/index.php?title=REST_API


#### Installing
```
$ pip install servicenow_rest
```


#### Example usage:
```python
import servicenow_rest.api as sn

s = sn.Client('instance_name', 'user_name', 'password')
s.table = 'incident'
try:
    res = s.get({'number': 'INC0012345'})
    print(res)
except sn.UnexpectedResponse as e:  # Unexpected server response (i.e. authentication error)
    print(e)
```


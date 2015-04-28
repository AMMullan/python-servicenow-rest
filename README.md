# servicenow-rest

The REST API is active by default in all instances, starting with the Eureka release.
Compatible with both Python 2 and 3.

For more info:
http://wiki.servicenow.com/index.php?title=REST_API


#### Example usage:
```
import servicenow_rest.api as sn

s = sn.Client('instance_name', 'user_name', 'password')
s.table = 'incident'
try:
    res = s.get({'number': 'INC0012345'})
    print(res)
except UnexpectedResponse as e:
    print(e)
except InvalidUsage as e:
    print(e)
```


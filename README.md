# python-servicenow-rest

The REST API is active by default in all instances, starting with the Eureka release.

Compatible with both Python 2 and 3. Tested with 2.7 and 3.4.

For more info, see:

http://wiki.servicenow.com/index.php?title=REST_API


#### Installing
```
$ pip install servicenow_rest
```


#### Usage

###### Connect

```python
import servicenow_rest.api as sn

s = sn.Client('instance_name', 'user_name', 'password')
```

###### Set table
```python
s.table = 'incident'
```

###### Get

```python
res = s.get({'number': 'INC0012345'})
print(res)
```


###### Create

```python
res = s.insert({'short_description': 'test', 'description': 'test'})
print(res['sys_id'])
```

###### Update

```python
res = s.get({'number': 'INC0012345'})
sys_id = res[0]['sys_id']
s.update({'comments': 'test', 'description': 'test'}, sys_id)
```

###### Delete

```python
res = s.get({'number': 'INC0012345'})
sys_id = res[0]['sys_id']
s.delete(sys_id)
```





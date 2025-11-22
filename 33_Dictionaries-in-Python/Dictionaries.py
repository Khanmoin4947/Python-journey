info={'name':'moin', 'age':17, 'status': 'student'}
print(info)
print(info['name'])

print(info.get('age')) #no error if 'age' doesnt exits

print(info.keys())
print(info.values())
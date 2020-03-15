import json
f = open('graph.json')
text = json.load(f)
node_list=set()
edge_node_list=set()
for i in range(29):
  node_list.add(text['visualization']['nodes'][i]['id'])
for i in range(35):
  edge_node_list.add(text['visualization']['edges'][i]['source'])
  edge_node_list.add(text['visualization']['edges'][i]['target'])

print(node_list==edge_node_list)
for i in range(29):
  print(i+1)
  print(text['visualization']['nodes'][i]['geo']['longitude'])
  print(text['visualization']['nodes'][i]['geo']['latitude'])
  print(text['visualization']['nodes'][i]['data']['名称'])
  print('------')

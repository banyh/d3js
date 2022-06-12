import math


def count_descendants(nodes, node_id):
    """
    設定 node_id 的 n_descendants 屬性，代表有幾個 descendant nodes (不包含自己)
    """
    n = nodes[node_id - 1]
    if 'n_descendants' in n:
        return n['n_descendants']

    if not n['children']:
        n['n_descendants'] = 0
        return n['n_descendants']

    c = sum([count_descendants(nodes, child_id) for child_id in n['children']])
    n['n_descendants'] = c + len(n['children'])
    return n['n_descendants']


def count_ascendants(nodes, node_id, ascendants):
    n = nodes[node_id - 1]
    n['ascendants'] = list(ascendants)
    for child_id in n['children']:
        count_ascendants(nodes, child_id, ascendants + [node_id])


def calculate_span_angle(nodes, node_id):
    """
    計算 children nodes 的 span_angle, offset_angle, level 屬性。
    當呼叫此函式時，我們假設 `nodes[node_id - 1]` 已經包含 span_angle, offset_angle, level 屬性。
    """
    n = nodes[node_id - 1]
    if not n['children']:
        return

    counts = [max(1, count_descendants(nodes, i)) for i in n['children']]
    total_counts = sum(counts)
    offset = n['offset_angle']
    for child_id, count in zip(n['children'], counts):
        child = nodes[child_id - 1]
        child['level'] = n['level'] + 1
        child['radius'] = child['level'] * 400
        child['span_angle'] = n['span_angle'] * (count / total_counts)
        child['offset_angle'] = offset
        child['suggest_x'] = child['level'] * 400 * math.cos(offset)
        child['suggest_y'] = child['level'] * 400 * math.sin(offset)
        offset += child['span_angle']
        calculate_span_angle(nodes, child_id)


def create_graph(data):
    nodes = []
    nodes_id = {}
    edges = []
    last_id = 1

    def _create_node(key, display_text, node_type):
        nonlocal last_id
        nodes_id[key] = last_id
        nodes.append({
            "key": key,
            "id": nodes_id[key],
            "display_text": display_text,
            "type": node_type,
            "radius": 0,
            "suggest_x": 0,
            "suggest_y": 0,
            "visible": True,
            "parents": [],
            "children": [],
        })
        last_id += 1
        return nodes_id[key]

    def _create_edge(source, target):
        edges.append(dict(source=source, target=target, value=1, visible=True))
        nodes[source - 1]['children'].append(target)
        nodes[target - 1]['parents'].append(source)

    for item in data:
        event_code_id = nodes_id.get(item['error'], 0)
        if not event_code_id:
            event_code_id = _create_node(item['error'], item['error'], 'event_code')

        subcode_id = nodes_id.get(item['subcode'], 0)
        if not subcode_id:
            subcode_id = _create_node(item['subcode'], item['subcode'], 'subcode')
            _create_edge(event_code_id, subcode_id)

        symptom_id = nodes_id.get(item['symptom_id'], 0)
        if not symptom_id:
            text = item['symptom_description'] + '\n' + item['symptom_title']
            symptom_id = _create_node(item['symptom_id'], text, 'symptom')
            _create_edge(subcode_id, symptom_id)

        for issue in item['issues']:
            issue_id = nodes_id.get(issue['jira_id'], 0)
            if not issue_id:
                key = issue['factory'] + '|' + issue['jira_id']
                text = issue['factory'] + '\n' + issue['jira_id']
                issue_id = _create_node(key, text, 'issue')
                _create_edge(symptom_id, issue_id)

        for cause in item['causes']:
            cause_id = nodes_id.get(cause['cause_id'], 0)
            if not cause_id:
                cause_id = _create_node(cause['cause_id'], cause['cause_title'], 'cause')
                _create_edge(symptom_id, cause_id)

            for proc in cause.get('procedures', []):
                text = proc['name'] + '\n' + proc['title']
                proc_id = _create_node(proc['name'], text, 'procedure')
                _create_edge(cause_id, proc_id)

                for part in proc.get('parts', []):
                    part_id = _create_node(part['id'], part['desc'], 'part')
                    _create_edge(proc_id, part_id)

                for tool in proc.get('tools', []):
                    tool_id = _create_node(tool['id'], tool['desc'], 'tool')
                    _create_edge(proc_id, tool_id)

    event_codes = [n for n in nodes if n['type'] == 'event_code']
    if len(event_codes) > 1:  # multiple event codes
        # 如果有多個 event codes，則創造一個 dummy node 作為 root node
        root_id = _create_node('root', 'root', 'root')
        for node in event_codes:
            _create_edge(root_id, node['id'])
    else:
        # 找到 root node，如果只有一個 event code，它就是 root node
        root_id = event_codes[0]['id']

    count_descendants(nodes, root_id)  # 設定所有 tree nodes 的 n_descendants

    count_ascendants(nodes, root_id, [])

    nodes[root_id - 1]['span_angle'] = math.pi / 12 * sum([n['type'] == 'subcode' for n in nodes])
    nodes[root_id - 1]['offset_angle'] = 0
    nodes[root_id - 1]['level'] = 0
    calculate_span_angle(nodes, root_id)

    for edge in edges:
        src, tgt = nodes[edge['source'] - 1], nodes[edge['target'] - 1]
        edge['value'] = math.sqrt((src['suggest_x'] - tgt['suggest_x']) ** 2 +
                                  (src['suggest_y'] - tgt['suggest_y']) ** 2)

    return {"nodes": nodes, "edges": edges}

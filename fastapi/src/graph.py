import math


def calculate_suggested_position(nodes, parent_id):
    def _count_descendants(n):
        c = sum([_count_descendants(nodes[child - 1]) for child in n['descendants']])
        return c + len(n['descendants'])

    parent_node = nodes[parent_id - 1]
    counts = [_count_descendants(nodes[i - 1]) for i in parent_node['descendants']]
    total_counts = sum(counts)
    if total_counts == 0:
        return
    for i, c in zip(parent_node['descendants'], counts):
        nodes[i - 1]['span_angle'] = parent_node['span_angle'] * (c / total_counts)
        calculate_suggested_position(nodes, i)


def create_graph(data):
    nodes = []
    nodes_id = {}
    edges = []
    last_id = 1

    def _create_node(key, display_text, node_type):
        nonlocal last_id
        nodes_id[key] = last_id
        nodes.append({
            "id": nodes_id[key],
            "display_text": display_text,
            "type": node_type,
            "suggest_x": 0,
            "suggest_y": 0,
            "ascendants": [],
            "descendants": [],
        })
        last_id += 1
        return nodes_id[key]

    def _create_edge(source, target):
        edges.append(dict(source=source, target=target, value=1))
        nodes[source - 1]['descendants'].append(target)
        nodes[target - 1]['ascendants'].append(source)

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
                text = issue['factory'] + '\n' + issue['jira_id']
                issue_id = _create_node(issue['jira_id'], text, 'issue')
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
        root_id = _create_node('root', 'root', 'root')
        for node in event_codes:
            _create_edge(root_id, node['id'])
    else:
        root_id = event_codes[0]['id']
    nodes[root_id - 1]['span_angle'] = 2 * math.pi
    calculate_suggested_position(nodes, root_id)

    return {"nodes": nodes, "edges": edges}

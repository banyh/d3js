test_data = [
    {
        "error": "WP-2C1D",
        "problem_id": 42131,
        "subcode": "8C010005",
        "symptom_description": "SYSTEM ERROR WP-2C1D",
        "symptom_id": 4551057,
        "symptom_title": "WS* COOLING WATER TEMP CONTROL MMDC: WAFER FLOW CONTROL: LCW PUMP ENABLED DRY OR NO FLOW ERROR",
        "causes": [
            {
                "cause_id": 4,
                "cause_title": "wafer stage PPL leak",
                "procedures": [
                    {
                        "destination": "Service",
                        "name": "cws754.rep",
                        "status": "Final",
                        "subsystem": "WaferStage",
                        "title": "REMOVE AND INSTALL LCW RETURN TEMP SENSOR IN MK4i PPL",
                        "type": "Replace",
                        "parts": [
                            {
                                "id": "SERV.646.47404",
                                "desc": "NXT WS MK4I PPL TEMP SENS ASSY",
                            },
                            {
                                "id": "SERV.502.31876",
                                "desc": "NXT WS MK4I PCA CONN SEAL SET",
                            }
                        ],
                        "tools": [
                            {
                                "id": "SERV.502.17463",
                                "desc": "CS SR GR4 TOOL TROLLEY",
                            },
                            {
                                "id": "4022.502.81530",
                                "desc": "NT WS BM3 SERVICE COVER KIT",
                            }
                        ]
                    }
                ]
            },
            {
                "cause_id": 4551058,
                "cause_title": "MORE CAUSES POSSIBLE [NXT3 ONLY]",
                "procedures": [
                    {
                        "destination": "Service",
                        "name": "cws383.oca",
                        "status": "Final",
                        "subsystem": "WaferStage",
                        "title": "NXT3&4 WS LCSW FLOW PROBLEM OR LCW PRESSURE SENSOR WIRING DEFECT",
                        "type": "Ocap",
                        "tools": [
                            {
                                "id": "SERV.640.55621",
                                "desc": "TDE CONNECTOR TOOLKIT",
                            },
                            {
                                "id": "4022.502.81530",
                                "desc": "NT WS BM3 SERVICE COVER KIT",
                            }
                        ]
                    }
                ]
            },
            {
                "cause_id": 25648264,
                "cause_title": "HR valve (too far) closed",
                "procedures": []
            }
        ],
        "issues": [
            {
                "factory": "F15B",
                "jira_id": "LIT1XVBEEA-197109",
                "event_cd": "WP-2C1D",
                "subcode": "8C010005",
                "actions": "",
                "is_useful": True,
                "tool_id": "YPAN03",
            },
            {
                "factory": "F15B",
                "jira_id": "LIT1XVBEEA-190894",
                "event_cd": "WP-2C1D",
                "subcode": "8C010005",
                "actions": "",
                "is_useful": True,
                "tool_id": "YPAN03",
            }
        ]
    }
];


def create_graph():
    nodes = []
    nodes_id = {}
    edges = []
    last_id = 1

    def _create_node(key, display_text, node_type):
        nonlocal last_id
        nodes_id[key] = last_id
        last_id += 1
        nodes.append({
            "id": nodes_id[key],
            "display_text": display_text,
            "type": node_type,
        })
        return nodes_id[key]

    for item in test_data:
        event_code_id = nodes_id.get(item['error'], 0)
        if not event_code_id:
            event_code_id = _create_node(item['error'], item['error'], 'event_code')

        subcode_id = nodes_id.get(item['subcode'], 0)
        if not subcode_id:
            subcode_id = _create_node(item['subcode'], item['subcode'], 'subcode')
            edges.append(dict(source=event_code_id, target=subcode_id, value=1))

        symptom_id = nodes_id.get(item['symptom_id'], 0)
        if not symptom_id:
            text = item['symptom_description'] + '\n' + item['symptom_title']
            symptom_id = _create_node(item['symptom_id'], text, 'symptom')
            edges.append(dict(source=subcode_id, target=symptom_id, value=1))

        for issue in item['issues']:
            issue_id = nodes_id.get(issue['jira_id'], 0)
            if not issue_id:
                text = issue['factory'] + '\n' + issue['jira_id']
                issue_id = _create_node(issue['jira_id'], text, 'issue')
                edges.append(dict(source=symptom_id, target=issue_id, value=1))

        for cause in item['causes']:
            cause_id = nodes_id.get(cause['cause_id'], 0)
            if not cause_id:
                cause_id = _create_node(cause['cause_id'], cause['cause_title'], 'cause')
                edges.append(dict(source=symptom_id, target=cause_id, value=1))

            for proc in cause.get('procedures', []):
                text = proc['name'] + '\n' + proc['title']
                proc_id = _create_node(proc['name'], text, 'procedure')
                edges.append(dict(source=cause_id, target=proc_id, value=1))

                for part in proc.get('parts', []):
                    part_id = _create_node(part['id'], part['desc'], 'part')
                    edges.append(dict(source=proc_id, target=part_id, value=1))

                for tool in proc.get('tools', []):
                    tool_id = _create_node(tool['id'], tool['desc'], 'tool')
                    edges.append(dict(source=proc_id, target=tool_id, value=1))

    return {"nodes": nodes, "edges": edges}

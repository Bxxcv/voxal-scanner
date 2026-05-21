def build_report(results):
    report = {
        'summary': {
            'total_vulns': 0,
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        },
        'findings': [],
        'exploit_commands': []
    }
    
    for module, data in results.items():
        if isinstance(data, dict):
            if data.get('vulnerable') or data.get('found'):
                report['summary']['total_vulns'] += 1
                report['findings'].append({
                    'module': module,
                    'details': data.get('details', data.get('found', [])),
                    'exploit_guide': data.get('exploit_guide', [])
                })
                for exp in data.get('exploit_guide', []):
                    report['exploit_commands'].append(exp)
    
    return report
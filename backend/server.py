#!/usr/bin/env python3
"""
VOCXAL Security Scanner - Backend Server
Flask API untuk vulnerability scanning
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import threading
import json
import os
import time
from scanner_engine import VulnerabilityScanner

app = Flask(__name__)
app.secret_key = "voxal_bypass_2024"
CORS(app)

scanner = VulnerabilityScanner()
scan_status = {}

@app.route('/api/scan', methods=['POST'])
def start_scan():
    """Start vulnerability scan for target URL"""
    data = request.json
    target_url = data.get('url')
    modules = data.get('modules', ['sqli', 'xss', 'lfi', 'admin', 'port', 'cms'])
    
    if not target_url:
        return jsonify({'error': 'URL required'}), 400
    
    scan_id = f"scan_{int(time.time())}"
    scan_status[scan_id] = {
        'status': 'scanning',
        'progress': 0,
        'results': {},
        'logs': []
    }
    
    # Run scan in background thread
    thread = threading.Thread(
        target=run_scan,
        args=(scan_id, target_url, modules)
    )
    thread.start()
    
    return jsonify({'scan_id': scan_id, 'status': 'started'})

def run_scan(scan_id, target_url, modules):
    """Execute scan modules"""
    results = {}
    total_modules = len(modules)
    
    for idx, module in enumerate(modules):
        scan_status[scan_id]['logs'].append(f"[*] Scanning {module} on {target_url}")
        scan_status[scan_id]['progress'] = ((idx + 1) / total_modules) * 100
        
        if module == 'sqli':
            results['sqli'] = scanner.scan_sqli(target_url)
        elif module == 'xss':
            results['xss'] = scanner.scan_xss(target_url)
        elif module == 'lfi':
            results['lfi'] = scanner.scan_lfi(target_url)
        elif module == 'admin':
            results['admin'] = scanner.find_admin_panels(target_url)
        elif module == 'port':
            results['port'] = scanner.scan_ports(target_url)
        elif module == 'cms':
            results['cms'] = scanner.detect_cms(target_url)
        
        scan_status[scan_id]['results'] = results
        
        if results.get(module, {}).get('vulnerable'):
            scan_status[scan_id]['logs'].append(
                f"[!] VULNERABILITY FOUND in {module}: {results[module].get('details')}"
            )
        else:
            scan_status[scan_id]['logs'].append(f"[-] {module}: No vulnerabilities found")
        
        time.sleep(0.5)
    
    scan_status[scan_id]['status'] = 'completed'
    scan_status[scan_id]['logs'].append("[+] Scan completed successfully!")

@app.route('/api/status/<scan_id>', methods=['GET'])
def get_status(scan_id):
    """Get scan status and results"""
    if scan_id not in scan_status:
        return jsonify({'error': 'Scan not found'}), 404
    
    return jsonify(scan_status[scan_id])

@app.route('/api/report/<scan_id>', methods=['GET'])
def generate_report(scan_id):
    """Generate detailed report"""
    if scan_id not in scan_status:
        return jsonify({'error': 'Scan not found'}), 404
    
    from report_builder import build_report
    report = build_report(scan_status[scan_id]['results'])
    return jsonify(report)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
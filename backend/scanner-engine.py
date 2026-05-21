import requests
import socket
import time
import re
from urllib.parse import urljoin, urlparse

class VulnerabilityScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'VOCXAL-Scanner/1.0'})
        self.timeout = 10

    def scan_sqli(self, target_url):
        results = {'vulnerable': False, 'details': [], 'exploit_guide': []}
        payloads = ["' OR '1'='1", "' UNION SELECT NULL--", "' AND SLEEP(5)--"]
        for p in payloads:
            try:
                test_url = f"{target_url}?id={p}"
                start = time.time()
                r = self.session.get(test_url, timeout=self.timeout)
                elapsed = time.time() - start
                if "mysql" in r.text.lower() or "sql" in r.text.lower():
                    results['vulnerable'] = True
                    results['details'].append(f"SQLi with {p}")
                    results['exploit_guide'].append({'method': 'Union SQLi', 'command': f"sqlmap -u '{test_url}' --dbs"})
                if elapsed > 4:
                    results['vulnerable'] = True
                    results['details'].append("Time-based SQLi")
                    results['exploit_guide'].append({'method': 'Time-based', 'command': f"sqlmap -u '{target_url}?id=1' --technique=T"})
            except:
                pass
        return results

    def scan_xss(self, target_url):
        results = {'vulnerable': False, 'details': [], 'exploit_guide': []}
        payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert(1)>"]
        for p in payloads:
            try:
                test_url = f"{target_url}?q={p}"
                r = self.session.get(test_url, timeout=self.timeout)
                if p in r.text or p.lower() in r.text.lower():
                    results['vulnerable'] = True
                    results['details'].append(f"XSS with {p}")
                    results['exploit_guide'].append({'method': 'Reflected XSS', 'command': f"curl '{test_url}'"})
            except:
                pass
        return results

    def scan_lfi(self, target_url):
        results = {'vulnerable': False, 'details': [], 'exploit_guide': []}
        payloads = ["../../../../etc/passwd", "../../../windows/win.ini"]
        for p in payloads:
            try:
                test_url = f"{target_url}?page={p}"
                r = self.session.get(test_url, timeout=self.timeout)
                if "root:x:" in r.text or "fonts" in r.text:
                    results['vulnerable'] = True
                    results['details'].append(f"LFI with {p}")
                    results['exploit_guide'].append({'method': 'LFI', 'command': f"curl '{test_url}'"})
            except:
                pass
        return results

    def find_admin_panels(self, target_url):
        results = {'found': [], 'exploit_guide': []}
        paths = ['admin', 'administrator', 'wp-admin', 'dashboard', 'login']
        for p in paths:
            test_url = urljoin(target_url, p)
            try:
                r = self.session.get(test_url, timeout=self.timeout)
                if r.status_code == 200:
                    results['found'].append(test_url)
                    results['exploit_guide'].append({'method': 'Admin panel found', 'command': f"hydra -l admin -P pass.txt {test_url} http-post-form"})
            except:
                pass
        return results

    def scan_ports(self, target_url):
        results = {'open_ports': [], 'exploit_guide': []}
        ports = [21,22,80,443,3306,8080]
        hostname = urlparse(target_url).hostname
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                if sock.connect_ex((hostname, port)) == 0:
                    results['open_ports'].append(port)
                    results['exploit_guide'].append({'method': f'Port {port} open', 'command': f"nmap -p {port} {hostname}"})
                sock.close()
            except:
                pass
        return results

    def detect_cms(self, target_url):
        results = {'cms': None, 'exploit_guide': []}
        sig = {'WordPress': '/wp-content/', 'Joomla': '/media/system/js/'}
        try:
            r = self.session.get(target_url, timeout=self.timeout)
            for cms, s in sig.items():
                if s in r.text:
                    results['cms'] = cms
                    results['exploit_guide'].append({'method': f'{cms} exploit', 'command': f"searchsploit {cms.lower()}"})
        except:
            pass
        return results

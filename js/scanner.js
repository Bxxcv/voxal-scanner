// VOCXAL Scanner Core - JavaScript Frontend

class VOCXALScanner {
    constructor() {
        this.apiBase = 'http://localhost:5000/api';
        this.currentScanId = null;
        this.scanInterval = null;
    }
    
    async startScan(targetUrl, modules) {
        const modal = document.getElementById('scanModal');
        const scanLog = document.getElementById('scanLog');
        const progressFill = document.querySelector('.progress-fill');
        
        modal.style.display = 'flex';
        scanLog.innerHTML = '<div class="log-entry">[VOCXAL] Initializing scan engine...</div>';
        
        try {
            const response = await fetch(`${this.apiBase}/scan`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: targetUrl, modules: modules })
            });
            
            const data = await response.json();
            this.currentScanId = data.scan_id;
            
            // Poll for results
            this.scanInterval = setInterval(async () => {
                const status = await this.getScanStatus();
                this.updateScanDisplay(status, scanLog, progressFill);
                
                if (status.status === 'completed') {
                    clearInterval(this.scanInterval);
                    setTimeout(() => {
                        this.generateReport();
                    }, 1000);
                }
            }, 2000);
            
        } catch (error) {
            scanLog.innerHTML += `<div class="log-entry error">[ERROR] ${error.message}</div>`;
        }
    }
    
    async getScanStatus() {
        const response = await fetch(`${this.apiBase}/status/${this.currentScanId}`);
        return await response.json();
    }
    
    updateScanDisplay(status, logElement, progressFill) {
        // Update progress
        progressFill.style.width = `${status.progress}%`;
        
        // Update logs
        if (status.logs && status.logs.length > 0) {
            const lastLog = status.logs[status.logs.length - 1];
            logElement.innerHTML += `<div class="log-entry">${this.escapeHtml(lastLog)}</div>`;
            logElement.scrollTop = logElement.scrollHeight;
        }
        
        // Update vulnerability count
        if (status.results) {
            let vulnCount = 0;
            for (let module in status.results) {
                if (status.results[module]?.vulnerable === true || 
                    status.results[module]?.found?.length > 0) {
                    vulnCount++;
                }
            }
            document.getElementById('vulnsFound').innerText = vulnCount;
        }
    }
    
    async generateReport() {
        const response = await fetch(`${this.apiBase}/report/${this.currentScanId}`);
        const report = await response.json();
        
        // Store report in localStorage for report page
        localStorage.setItem('voxal_report', JSON.stringify(report));
        
        // Redirect to report page
        window.location.href = 'report.html';
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize scanner
const scanner = new VOCXALScanner();

document.getElementById('startScan').addEventListener('click', async () => {
    const targetUrl = document.getElementById('targetUrl').value;
    const modules = Array.from(document.querySelectorAll('.scan-module:checked'))
        .map(cb => cb.value);
    
    if (!targetUrl) {
        alert('Please enter a target URL');
        return;
    }
    
    await scanner.startScan(targetUrl, modules);
});

// Update stats
let scansCount = localStorage.getItem('scansCount') || 0;
document.getElementById('scansCount').innerText = scansCount;
document.getElementById('activeUsers').innerText = Math.floor(Math.random() * 100) + 50;
import { getReport, scenarios } from './scenarios.mjs';

function appendElement(parent, tag, text, className) {
    const element = document.createElement(tag);
    element.textContent = text;
    if (className) element.className = className;
    parent.append(element);
    return element;
}

const scenarioSelect = document.getElementById('scenario');
const scenarioList = document.getElementById('scenario-list');
const reportTitle = document.getElementById('report-title');

if (scenarioSelect) {
    for (const { id, title } of scenarios) {
        scenarioSelect.add(new Option(title, id));
    }
    document.getElementById('open-report').disabled = false;
}

if (scenarioList) {
    for (const { id, title, description, findings } of scenarios) {
        const card = appendElement(scenarioList, 'article', '', 'feature-card');
        appendElement(card, 'h2', title);
        appendElement(card, 'p', description);
        const link = appendElement(card, 'a', `Lihat laporan ${title} (${findings.length} temuan)`, 'text-link');
        link.href = `report.html?${new URLSearchParams({ scenario: id })}`;
    }
}

if (reportTitle) {
    const report = getReport(new URLSearchParams(location.search).get('scenario'));
    const intro = document.getElementById('report-intro');
    const findingsList = document.getElementById('findings');

    if (!report) {
        reportTitle.textContent = 'Skenario tidak ditemukan';
        intro.textContent = 'Pilih skenario dari dashboard untuk membuka laporan.';
    } else {
        reportTitle.textContent = report.title;
        intro.textContent = `${report.description} Total: ${report.findings.length} temuan sintetis.`;
        if (report.findings.length === 0) {
            appendElement(findingsList, 'p', 'Tidak ada temuan dalam skenario ini. Ini bukan bukti bahwa suatu sistem aman.');
        }
        for (const { title, severity, remediation } of report.findings) {
            const card = appendElement(findingsList, 'article', '', 'feature-card');
            appendElement(card, 'h2', title);
            appendElement(card, 'p', `Keparahan: ${severity}`, 'severity');
            appendElement(card, 'p', `Remediasi: ${remediation}`);
        }
    }
}

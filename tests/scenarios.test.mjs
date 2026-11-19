import assert from 'node:assert/strict';
import { test } from 'node:test';
import { scenarios, getReport } from '../js/scenarios.mjs';

test('each scenario has a unique ID and reports its own fixture', () => {
    assert.equal(new Set(scenarios.map(({ id }) => id)).size, scenarios.length);
    for (const scenario of scenarios) {
        assert.equal(getReport(scenario.id), scenario);
        for (const finding of scenario.findings) {
            assert.ok(finding.title && finding.severity && finding.remediation);
        }
    }
});

test('catalog and baseline cover finding and empty states', () => {
    assert.ok(getReport('catalog').findings.length > 0);
    assert.equal(getReport('baseline').findings.length, 0);
});

test('unknown scenario IDs do not produce a report', () => {
    for (const id of [null, '', 'unknown', 'constructor', 'https://example.com']) {
        assert.equal(getReport(id), undefined);
    }
});

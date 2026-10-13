// Evaluate a .dc.html page's renderVals() and print the result as JSON (functions -> null).
const fs = require('fs');
const file = process.argv[2];
const state = JSON.parse(process.argv[3] || '{}');
const src = fs.readFileSync(file, 'utf8');
const m = src.match(/<script type="text\/x-dc" data-dc-script[^>]*>([\s\S]*?)<\/script>/);
if (!m) { console.log('{}'); process.exit(0); }
class DCLogic { constructor() { this.props = {}; this.state = {}; } setState() {} forceUpdate() {} }
const Component = new Function('DCLogic', m[1] + '\nreturn Component;')(DCLogic);
const c = new Component();
c.props = {};
c.state = state;
const vals = c.renderVals();
console.log(JSON.stringify(vals, (k, v) => (typeof v === 'function' ? null : v)));

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'practice.html'), 'utf8');
const bankText = html.match(/<script type="application\/json" id="pp-bank">([\s\S]*?)<\/script>/)[1];
const bank = JSON.parse(bankText);
const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
const elements = Object.fromEntries(ids.map(id => [id, {
  value: '', textContent: '', hidden: false, handlers: {},
  addEventListener(name, handler) { this.handlers[name] = handler; },
  focus() {},
}]));
elements['pp-bank'].textContent = bankText;
elements['python-practice'].querySelector = selector => elements[selector.slice(1)] || null;
const context = {
  document: { getElementById: id => elements[id] || null },
  window: {}, Date, console,
};
vm.createContext(context);
const script = [...html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)]
  .find(match => !match[1].includes('application/json'))[2];
vm.runInContext(script, context, { timeout: 1000 });
const { tokens } = context.window.__pythonPracticeTest;
assert.equal(tokens('x = "a b"'), tokens("x='a b'"));
assert.notEqual(tokens('x = "a b"'), tokens('x = "ab"'));
assert.notEqual(tokens('Counter(names)'), tokens('counter(names)'));
assert.equal(tokens('"unfinished'), null);
for (const question of bank) {
  for (const answer of question.answers) {
    assert.notEqual(tokens(answer), null);
    assert.equal(tokens(`  ${answer}  `), tokens(answer));
  }
}
assert.equal(elements['pp-topic'].textContent, '빈 리스트');
elements['pp-answer'].value = '[]';
elements['pp-check'].handlers.click({ preventDefault() {} });
assert.match(elements['pp-feedback'].textContent, /맞았/);
assert.match(elements['pp-progress'].textContent, /1\/50/);
elements['pp-next'].handlers.click();
assert.equal(elements['pp-topic'].textContent, 'append');
elements['pp-answer'].value = 'appned';
elements['pp-check'].handlers.click({ preventDefault() {} });
assert.match(elements['pp-feedback'].textContent, /append/);
elements['pp-reveal'].handlers.click();
assert.equal(elements['pp-complete'].hidden, false);
elements['pp-answer'].value = 'append';
elements['pp-check'].handlers.click({ preventDefault() {} });
assert.match(elements['pp-progress'].textContent, /복습 1/);
elements['pp-review'].handlers.click();
assert.equal(elements['pp-topic'].textContent, 'append');
elements['pp-stage'].value = '5';
elements['pp-stage'].handlers.change();
assert.match(elements['pp-topic'].textContent, /추가/);
console.log(`PASS: ${bank.length} questions; token rules, grading, navigation, help and review interactions.`);

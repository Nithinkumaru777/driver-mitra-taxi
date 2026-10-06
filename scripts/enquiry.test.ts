// npm test — enquiry validation and the WhatsApp text (node:test, no extra deps).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseMobile, validateEnquiry, submitEnquiry } from '../src/scripts/enquiry.ts';
import { getCopy } from '../src/content/site.ts';

const t = getCopy();

test('parseMobile accepts real Indian mobiles in common formats', () => {
  for (const ok of ['9876543210', '98765 43210', '+91 98765-43210', '919876543210', '09876543210'])
    assert.equal(parseMobile(ok), '9876543210', ok);
  assert.equal(parseMobile('6000000001'), '6000000001');
});

test('parseMobile blocks bad numbers', () => {
  for (const bad of ['', '987654321', '98765432100', '5876543210', '0123456789', '9999999999', 'abcdefghij', '+1 9876543210'])
    assert.equal(parseMobile(bad), null, bad);
});

test('validateEnquiry flags every missing field and passes a complete one', () => {
  const empty = { name: ' ', mobile: '123', city: '', plan: '', licence: '', message: '' };
  assert.deepEqual(Object.keys(validateEnquiry(empty, t)).sort(), ['city', 'licence', 'mobile', 'name', 'plan']);
  assert.deepEqual(validateEnquiry({ ...empty, name: 'A', mobile: '9876543210', city: 'B', plan: '3', licence: 'Yes' }, t), {});
});

test('submitEnquiry opens wa.me with the details pre-filled', () => {
  const href = submitEnquiry(
    { name: ' Ramesh ', mobile: '+91 98765 43210', city: 'Bengaluru', plan: '4', licence: 'Yes', message: 'Call after 6 & ask for R' },
    t,
  );
  const url = new URL(href);
  assert.equal(url.origin, 'https://wa.me');
  assert.equal(
    url.searchParams.get('text'),
    [
      'New enquiry from the Driver Mitra website',
      '',
      'Name: Ramesh',
      'Mobile number: +91 98765 43210',
      'City: Bengaluru',
      'Preferred plan: 4 Years Flexible Plan',
      'Do you have a commercial driving licence/badge? Yes',
      'Message: Call after 6 & ask for R',
    ].join('\n'),
  );
  // Empty message → no Message line.
  const text = new URL(submitEnquiry({ name: 'A', mobile: '9876543210', city: 'B', plan: '3', licence: 'No', message: '' }, t)).searchParams.get('text')!;
  assert.ok(!text.includes('Message:'));
});

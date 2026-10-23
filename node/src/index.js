/**
 * CC Generator — Luhn-valid test credit card numbers.
 */

function luhnOk(number) {
  const digits = number.replace(/\D/g, '').split('').reverse().map(Number);
  let total = 0;
  let alt = false;
  for (const n of digits) {
    let val = n;
    if (alt) {
      val *= 2;
      if (val > 9) val -= 9;
    }
    total += val;
    alt = !alt;
  }
  return total % 10 === 0;
}

function luhnComplete(prefix, length) {
  const needed = length - 1 - prefix.length;
  let body = prefix;
  for (let i = 0; i < needed; i++) {
    body += Math.floor(Math.random() * 10);
  }
  for (let d = 0; d <= 9; d++) {
    const cand = body + d;
    if (luhnOk(cand)) return cand;
  }
  throw new Error('luhn: no check digit found');
}

const VISA_BINS = [
  { bin: '415464440635', brand: 'visa', lengths: [16], cvv: 3 },
  { bin: '400000', brand: 'visa', lengths: [16], cvv: 3 },
];

const UNIONPAY_BINS = [
  { bin: '6233586370', brand: 'unionpay', lengths: [16, 17, 18, 19], cvv: 3 },
];

const MASTERCARD_BINS = [
  { bin: '555555', brand: 'mastercard', lengths: [16], cvv: 3 },
];

const AMEX_BINS = [
  { bin: '378282', brand: 'amex', lengths: [15], cvv: 4 },
];

const DISCOVER_BINS = [
  { bin: '601111', brand: 'discover', lengths: [16], cvv: 3 },
];

const DEFAULT_BINS = [...VISA_BINS, ...UNIONPAY_BINS, ...MASTERCARD_BINS, ...AMEX_BINS, ...DISCOVER_BINS];

function genCard(opts = {}) {
  const bins = opts.bins || DEFAULT_BINS;
  const spec = opts.binSpec || bins[Math.floor(Math.random() * bins.length)];
  const length = spec.lengths[Math.floor(Math.random() * spec.lengths.length)];
  const number = luhnComplete(spec.bin, length);
  const month = String(Math.floor(Math.random() * 12) + 1).padStart(2, '0');
  const year = 2026 + Math.floor(Math.random() * 5) + 2;
  const cvvLen = spec.cvv || 3;
  let cvv = '';
  for (let i = 0; i < cvvLen; i++) cvv += Math.floor(Math.random() * 10);
  return {
    number,
    bin: spec.bin,
    brand: spec.brand,
    expMonth: month,
    expYear: String(year),
    exp: `${month}/${String(year).slice(-2)}`,
    cvv,
    luhn: luhnOk(number),
  };
}

function genCards(count = 1, opts = {}) {
  const out = [];
  for (let i = 0; i < count; i++) out.push(genCard(opts));
  return out;
}

const FIRST_NAMES = [
  'Marcus', 'Delaney', 'Elena', 'Tobias', 'Priya', 'Owen', 'Nadia', 'Felix',
  'Iris', 'Jonah', 'Celine', 'Rafael', 'Maya', 'Dorian', 'Sofia',
];
const LAST_NAMES = [
  'Whitfield', 'Navarro', 'Lindqvist', 'Okafor', 'Brennan', 'Halvorsen',
  'Castellano', 'Duarte', 'Mercer', 'Ashford', 'Kowalski', 'Ferreira',
];
const STREETS = [
  'Sunset Ridge Drive', 'Maple Court', 'Easton Avenue', 'Willow Bend Road',
  'Chestnut Street', 'Harbor View Lane', 'Kingsway Boulevard',
];
const CITIES = [
  ['Austin', 'Texas', '78701'],
  ['Denver', 'Colorado', '80202'],
  ['Portland', 'Oregon', '97204'],
  ['Raleigh', 'North Carolina', '27601'],
  ['Boise', 'Idaho', '83702'],
  ['Tampa', 'Florida', '33602'],
];

function rand(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function genIdentity() {
  const [city, state, zip] = rand(CITIES);
  return {
    name: `${rand(FIRST_NAMES)} ${rand(LAST_NAMES)}`,
    company: 'N/A',
    address: `${Math.floor(Math.random() * 9800 + 100)} ${rand(STREETS)}`,
    city,
    state,
    zip,
    country: 'US',
    countryCode: '1',
    phone: `${Math.floor(Math.random() * 789 + 201)}${Math.floor(Math.random() * 800 + 200)}${Math.floor(Math.random() * 9000 + 1000)}`,
  };
}

module.exports = {
  luhnOk,
  luhnComplete,
  genCard,
  genCards,
  genIdentity,
  VISA_BINS,
  UNIONPAY_BINS,
  MASTERCARD_BINS,
  AMEX_BINS,
  DISCOVER_BINS,
  DEFAULT_BINS,
};

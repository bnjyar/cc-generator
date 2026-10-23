#!/usr/bin/env node
const { genCards, genIdentity, luhnOk, DEFAULT_BINS } = require('./index');

function parseArgs(argv) {
  const args = argv.slice(2);
  const get = (flag) => {
    const i = args.indexOf(flag);
    return i !== -1 ? args[i + 1] : undefined;
  };
  const has = (flag) => args.includes(flag);
  return {
    count: parseInt(get('--count') || '1', 10),
    bin: get('--bin'),
    brand: get('--brand'),
    length: get('--length') ? parseInt(get('--length'), 10) : undefined,
    identity: has('--identity'),
    json: has('--json'),
  };
}

function main() {
  const a = parseArgs(process.argv);

  let bins = DEFAULT_BINS;
  if (a.brand) {
    bins = bins.filter(b => b.brand === a.brand);
  }
  if (a.bin) {
    bins = [{ bin: a.bin, brand: 'custom', lengths: [a.length || 16], cvv: 3 }];
  }

  const results = genCards(a.count, { bins });
  for (const c of results) c.luhn = luhnOk(c.number);

  const ident = a.identity ? genIdentity() : null;

  if (a.json) {
    const out = { cards: results };
    if (ident) out.identity = ident;
    console.log(JSON.stringify(out, null, 2));
  } else {
    for (const c of results) {
      console.log(`${c.number}  ${c.exp}  ${c.cvv}  ${c.brand}  luhn=${c.luhn}`);
    }
    if (ident) {
      console.log(`Identity: ${ident.name}, ${ident.address}, ${ident.city} ${ident.zip}`);
    }
  }
}

main();

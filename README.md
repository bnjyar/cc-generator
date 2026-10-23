# cc-generator

Generate Luhn-valid test credit card numbers and fake identities.

Available for **Python** and **Node.js**.

## Python

```bash
cd python
pip install -e .
```

```python
from cc_generator import gen_card, gen_identity, luhn_ok

card = gen_card()
print(card["number"], card["exp"], card["cvv"])
assert luhn_ok(card["number"])

ident = gen_identity()
print(ident["name"], ident["address"])
```

## Node.js

```bash
cd node
npm install
```

```javascript
const { genCard, genIdentity, luhnOk } = require('cc-generator');

const card = genCard();
console.log(card.number, card.exp, card.cvv);
console.assert(luhnOk(card.number));

const ident = genIdentity();
console.log(ident.name, ident.address);
```

## CLI

Python:
```bash
cc-gen --count 3 --brand visa --json
```

Node:
```bash
node src/cli.js --count 3 --brand visa --json
```

# Student Robotics Inventory Import

Assets and History from the Student Robotics Inventory can be imported into PyInv.

You will need to parse the SR Inventory using [srobo-inv-parser](https://github.com/pyinv/srobo-inv-parser).

## Parse the Inventory

```bash
git clone https://github.com/pyinv/srobo-inv-parser.git
cd srobo-inv-parser
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

# Clone the Inventory
git clone https://github.com/srobo/inventory.git

# Parse the tree
cd inventory
python3 ../json_dump.py
cd ..
stat inv.json  # inv.json is generated

# Parse the History
mkdir changesets
python3 ./traverse_commits inventory
```

## Import Into PyInv

```bash
./manage.py srobo_import ../../srobo-inv-parser/inv.json
./manage.py srobo_import_history ../../srobo-inv-parser/changesets
./manage.py srobo_import_timestamps
```
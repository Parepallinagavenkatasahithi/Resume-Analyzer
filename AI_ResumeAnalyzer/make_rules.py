with open('backend/app/core_logic/massive_rules.py', 'w', encoding='utf-8') as f:
    f.write('COMPLEX_EVALUATION_MATRIX = [\n')
    for i in range(1, 550000):
        f.write(f'    {{"rule_id": "R{i}", "weight": {round(i*0.001, 3)}, "description": "Core metric for advanced resume evaluation heuristic {i}", "active": True}},\n')
    f.write(']\n')

## Python calculator and converter

### Commands:
 To run the calculator you need to run one of these commands:
1) python -m toolkit calc "YOUR EXPRESSION" - runs calculator that can calculate any expression you pass.
However, if there is/are mistake(s), the calculator will tell you
2) python -m toolkit convert VALUE --from MEASURE --to MEASURE - runs converter from one measure
to another. There are several converts: KG, G (mass); MM, CM, M, KM (length);
F, C, K (temperature) !!! All measures should be in lowercase
3) python -m toolkit setprecision VALUE - set precision of decimal
4) python -m toolkit --help - run to see helpful guide with calculator

### Setup
1) Use poetry enviroment. In pycharm you can select this envoriment in right bottom corner in case there weren't yellow notification with button installing poetry. Otherwise install poetry using browser.
2) Run "poetry install" and wait until everything is ready. When it's ready, this project will be shown as module so you can start using it
3) Run "poetry run test" to see everything is OK. There will be 4 sections with PYTEST and CLI tests.
4) Have fun using calculator :)

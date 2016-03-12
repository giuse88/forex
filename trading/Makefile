

backtest: 
	python ./apps/backtest.py 

test:
	@green -vv

test-watch:
	@fswatch --batch-marker --event Updated -xr -l 10 . | xargs -n1 -I{}  green -vv


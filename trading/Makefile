
test:
	@green -vv

test-watch:
	@fswatch --batch-marker --event Updated -xr -l 10 . | xargs -n1 -I{}  green -vv


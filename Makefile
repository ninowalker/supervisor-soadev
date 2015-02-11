PATH := env/bin:$(PATH)
export PATH

CFG = test_supervisorsoadev/supervisord.conf
CTL = supervisorctl -c $(CFG)

env: env/bin/activate
env/bin/activate: setup.py dev_requirements.txt
	test -f $@ || virtualenv --no-site-packages env
	. $@; pip install -e . -r dev_requirements.txt
	touch $@

test: env
	python test_supervisorsoadev/run_tests.py

cli_shutdown shutdown stop: $(CFG)
	$(CTL) shutdown

cli_test: $(CFG)
	supervisord -c $(CFG)
	$(CTL) status
	$(CTL) status g2 g1
	$(CTL) shutdown

cli_run:
	supervisord -c $(CFG) || true
	$(CTL)

ifeq ("$(VIRTUAL_ENV)", "")
  ENV=. env/bin/activate;
endif

update:
	$(ENV) pip install --upgrade pip wheel setuptools
	$(ENV) pip install ndg-httpsclient
	$(ENV) pip install -r ./requirements.txt

listdepends:
	$(ENV) pip list|cut -d\  -f1|while read x; do echo $$x $$(pip show $$x|grep Requires); done

scrape:
	$(ENV) python -u ./scraper/scrape.py | tee data/whisky.json

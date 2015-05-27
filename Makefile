config:
	@if [ ! -d ~/.rdb ] ; \
	then \
		mkdir ~/.rdb ; \
		cp setup/config ~/.rdb/ ; \
		cp setup/localdatabase ~/.rdb/ ; \
	else \
		echo '~/.rdb already exists.' ; \
	fi ;
install:
	python setup.py install

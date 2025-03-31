PREFIX=debian/python3-cyberfusion-queue-support/

install:
	mkdir -p $(PREFIX)usr/share/queue-support/

	cp alembic.debian.ini $(PREFIX)usr/share/queue-support/alembic.ini

	rsync -a migrations/ $(PREFIX)usr/share/queue-support/migrations/


uninstall:
	rm -r $(PREFIX)usr/share/queue-support/

clean:
	echo "NOP"


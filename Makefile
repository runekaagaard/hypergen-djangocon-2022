practice-run:
	mkdir -p past
	cp booking/views.py booking/views_finished.py
	cp -b booking/views.py past/
	cp booking/views_template.py booking/views.py
	git commit -am "New practice run"

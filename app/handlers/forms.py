import flask

from app.auth_password.decorators import login_required
from app import forms
from app.repositories import posts as posts_repository
from app.repositories import topics as topics_repository

@login_required
def new_post():
	new_post_form = forms.Post(flask.request.form)

	if new_post_form.validate():
		# return flask.redirect(url_for('post', post_id=new_post_id))

		topic_id = new_post_form.topic_id.data

		new_post = posts_repository.create(
			new_post_form.title.data,
			new_post_form.content.data,
			topic_id=topic_id)

		if topic_id:
			return flask.redirect(flask.url_for('topic', topic_id=topic_id))

		return flask.redirect(flask.url_for('recent'))

@login_required
def new_topic():
	new_topic_form = forms.NewTopic(flask.request.form)

	if new_topic_form.validate():
		new_topic = topics_repository.create(
			new_topic_form.title.data,
			new_topic_form.description.data,
		)
		return flask.redirect(flask.url_for('topics'))

@login_required
def edit_post(post_id):
	edit_post_form = forms.Post(flask.request.form)
	if edit_post_form.validate():
		update_data = {
			'id': post_id,
			'title': edit_post_form.title.data,
			'content': edit_post_form.content.data,
		}
		posts_repository.update_post(update_data)
		return flask.redirect(flask.url_for('post', post_id=post_id))

	flask.abort(400, "Form information was invalid")
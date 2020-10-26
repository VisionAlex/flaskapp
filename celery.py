from celery import Celery

celery_app = Celery('FlaskApp',
				broker='redis://localhost:6379',
				backend='redis://localhost:6379',
				include=['FlaskApp.tasks'])

if __name__ == '__main__':
	celery_app.start()
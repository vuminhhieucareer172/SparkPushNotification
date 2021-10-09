from sqlalchemy import Boolean, Column, Enum, VARCHAR, INTEGER, TEXT

from database import Model


class User(Model):
    __tablename__ = "dbstreaming_job_stream"

    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    job_name = Column(VARCHAR(50), nullable=False)
    table_streaming = Column(VARCHAR(50), nullable=False)
    table_query = Column(VARCHAR(50), nullable=False)
    topic_kafka_input = Column(VARCHAR(50), nullable=False)
    topic_kafka_output = Column(VARCHAR(50), nullable=False)
    config = Column(VARCHAR(255), nullable=False)
    status = Column(Enum('RUNNING', 'STOP', 'ERROR'), nullable=False, default='RUNNING')
    enabled = Column(Boolean, nullable=False, default=True)
    time = Column(VARCHAR(50), nullable=False, default='0 0 * * *')
    template = Column(VARCHAR(255), nullable=False)
    log = Column(TEXT)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def to_full_json(self):
        return dict(
            id=self.id,
            job_name=self.job_name,
            config=self.config,
            status=self.status,
            enabled=self.enabled,
            time=self.time,
            template=self.template,
            log=self.log,
        )

    @staticmethod
    def from_json(json_post):
        return User(
            job_name=json_post.get('job_name'),
            config=json_post.get('config'),
            status=json_post.get('status'),
            enabled=json_post.get('enabled'),
            time=json_post.get('time'),
            template=json_post.get('template'),
            log=json_post.get('log'),
        )

from sqlalchemy import Boolean, Column, Enum, VARCHAR, INTEGER
from sqlalchemy.dialects.mysql import LONGTEXT

from database import Model


class Job(Model):
    __tablename__ = "dbstreaming_job_stream"

    id = Column('id', INTEGER, primary_key=True, index=True, autoincrement=True)
    job_name = Column('job_name', VARCHAR(50), nullable=False)
    config = Column('config', VARCHAR(255), nullable=False)
    status = Column('status', Enum('RUNNING', 'STOP', 'ERROR'), nullable=False, default='RUNNING')
    enabled = Column('enabled', Boolean, nullable=False, default=True)
    time = Column('time', VARCHAR(50), nullable=False, default='0 0 * * *')
    template = Column('template', VARCHAR(255), nullable=False)
    log = Column('log', LONGTEXT)

    def __init__(self, **kwargs):
        super(Job, self).__init__(**kwargs)

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
        return Job(
            job_name=json_post.get('job_name'),
            config=json_post.get('config'),
            status=json_post.get('status'),
            enabled=json_post.get('enabled'),
            time=json_post.get('time'),
            template=json_post.get('template'),
            log=json_post.get('log'),
        )

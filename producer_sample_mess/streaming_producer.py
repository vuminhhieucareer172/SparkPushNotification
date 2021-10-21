import json

from confluent_kafka import Consumer, Producer
from constants.constants import KAFKA_URI, TOPIC_JOB
from kafka import KafkaProducer

producer = Producer({'bootstrap.servers': '10.0.2.5:9092'})

mess = {"name": "Viện Nghiên cứu Dữ liệu lớn - VinBigdata",
        "job_title": "Fresher Engineer (Python, Java)",
        "address": "Century Tower, T14, Khu đô thị Times City, 458 Minh Khai, Hai Ba Trung, Ha Noi",
        "job_description": "- Tham gia vào quá trình xây dựng các sản phẩm ứng dụng trí tuệ nhân tạo, trợ lý ảo AI hoạt "
                           "động trên thiết bị thông minh, phương tiện thông minh, nhà thông minh, thành phố và khu nghỉ dưỡng thông minh",
        "skill_experience": "- Kỹ năng lập trình, phát triển phần mềm\n - Hiểu biết cơ bản về AI, cách đóng gói phần mềm sử dụng AI.",
        "benefit": "- Được ưu đãi khi sử dụng dịch vụ và mua sản phẩm của tập đoàn như: VinFast, VinMart/VinMart+, VinPearl, VinMec, VinSchool.",
        "salary": 214748364800
        }

# mess = {"type": str(type("dgasdg"))}
a = json.dumps(mess)
producer.produce(TOPIC_JOB, a)
producer.flush()

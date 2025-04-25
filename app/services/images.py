from app.models import db, Image

# 이미지 생성
def create_image(url, image_type):
    new_image = Image(url=url, image_type = image_type)
    db.session.add(new_image)
    db.session.commit()
    return new_image.id

# 모든 이미지 조회
def get_all_image():
    return  [image.to_dict() for image in Image.query.all()]

# 특정 이미지 조회 
def get_image_by_id(image_id):
    image = Image.query.get(image_id)
    return image
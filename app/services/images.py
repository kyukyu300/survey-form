from app.models import db, Image

def create_image(url):
    new_image = Image(url=url)
    db.session.add(new_image)
    db.session.commit()
    return new_image.to_dict

def get_all_image(url):
    return  [Image.to_dict() for image in Image.query.all()]
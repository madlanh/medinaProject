from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text('ALTER TABLE organisasi ADD COLUMN jumlah INT DEFAULT 0'))
        print('Added jumlah column')
    except Exception as e:
        print(f'jumlah: {e}')
    
    try:
        db.session.execute(text("ALTER TABLE organisasi ADD COLUMN emoji VARCHAR(10) DEFAULT ''"))
        print('Added emoji column')
    except Exception as e:
        print(f'emoji: {e}')
    
    db.session.commit()
    print('Done!')

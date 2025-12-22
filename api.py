from app import create_app

import os
print("Isi folder app/routes:", os.listdir('app/routes'))
# Jika public ada, cek isinya
if 'public' in os.listdir('app/routes'):
    print("Isi folder app/routes/public:", os.listdir('app/routes/public'))

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

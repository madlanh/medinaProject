from datetime import datetime

def categorize_agenda(agenda_list):
    past = []
    today = []
    future = []
    current_date = datetime.now().date()
    
    for item in agenda_list:
        # item is an SQLAlchemy object, so we access attributes directly
        # We'll add display attributes dynamically for the template
        item.display_date = item.tanggal.strftime('%d %b %Y')
        item.day = item.tanggal.strftime('%d')
        item.month = item.tanggal.strftime('%b')
        
        item_date = item.tanggal.date() if isinstance(item.tanggal, datetime) else item.tanggal
        
        if item_date < current_date:
            past.append(item)
        elif item_date == current_date:
            today.append(item)
        else:
            future.append(item)
            
    return past, today, future

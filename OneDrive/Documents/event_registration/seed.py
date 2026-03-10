from app import app, db, Event, Admin

with app.app_context():
    # Delete existing data for a clean start
    Event.query.delete()
    db.session.commit()

    # Add sample events
    events = [
        Event(
            event_name='AI & Future Tech Summit', 
            date='Oct 15, 2024 at 10 AM', 
            location='Convention Center, NY', 
            description='Join industry leaders and innovators for a deep dive into the future of artificial intelligence, machine learning, and automation. This summit features keynote speakers from top tech companies, interactive workshops, and networking opportunities that you won\'t want to miss.'
        ),
        Event(
            event_name='Web Developers Meetup', 
            date='Nov 05, 2024 at 6 PM', 
            location='Tech Hub, San Francisco', 
            description='A casual gathering for web developers of all skill levels. We will discuss the latest trends in frontend frameworks, share tips on performance optimization, and enjoy some pizza and drinks. Whether you use React, Vue, or Vanilla JS, come connect with fellow developers.'
        ),
        Event(
            event_name='Startup Pitch Night', 
            date='Dec 12, 2024 at 7 PM', 
            location='Innovation Lab, Chicago', 
            description='Watch 10 promising startups pitch their ideas to a panel of expert judges and investors. This is a great opportunity to get inspired, learn what makes a successful pitch, and network with entrepreneurs. The winning startup will receive a significant seed investment.'
        )
    ]
    
    for event in events:
        db.session.add(event)
        
    db.session.commit()
    print("Database seeded successfully with sample events.")

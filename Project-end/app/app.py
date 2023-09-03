import os
import pandas as pd
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)




class ReviewBase(db.Model):
    __abstract__ = True  # This indicates to SQLAlchemy that it shouldn't be treated as a model on its own
    ID = db.Column(db.Integer, primary_key=True)
    profile_name = db.Column(db.String(100), nullable=True)
    Product_name = db.Column(db.String(300), nullable=True)
    price = db.Column(db.Float, nullable=False)
    rating_stars = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    review_rating = db.Column(db.Float, nullable=False)
    review_title = db.Column(db.String(200), nullable=False)
    review_content = db.Column(db.Text, nullable=True)
    sentiment_scores = db.Column(db.String(500), nullable=True)  # This is a JSON structure
    positive_score = db.Column(db.Float, nullable=True)
    # Add other columns based on your CSV structure

class MouseReview(ReviewBase):
    pass
class MonitorReview(ReviewBase):
    pass
class HeadphoneReview(ReviewBase):
    pass
class KeyboardReview(ReviewBase):
    pass

def load_csv_to_db(filepath, model):
    if not model.query.first():  # Check if data already exists to avoid duplication
        df = pd.read_csv(filepath)
        for index, row in df.iterrows():
            try:
                if pd.isna(row.get('Profile Names', None)) or pd.isna(row.get('Product name', None)):
                    print(f"Skipping row {index}: Missing 'Profile Names' or 'Product name'")
                    continue  # Skip this row
                
                review = model(
                    ID=row.get('ID', None),
                    profile_name=row.get('Profile Names', None),
                    Product_name=row.get('Product name', None),
                    price=row.get('Price', None),
                    rating_stars=row.get('Rating stars', None),
                    link=row.get('Link', None),
                    image=row.get('image', None),
                    review_rating=row.get('Review Ratings', None),
                    review_title=row.get('Review Title', None),
                    review_content=row.get('Review Content', ''),
                    sentiment_scores=row.get('Sentiment Scores', None),
                    positive_score=row.get('Positive Score', None)
                )
                db.session.add(review)
                
            except Exception as e:
                print(f"Error inserting row {index}: {e}")
                
        try:  # Try to commit changes to the database
            db.session.commit()
        except IntegrityError as e:  # Catch IntegrityError
            db.session.rollback()  # Rollback transaction
            print(f"Integrity Error occurred: {e}")


def load_data_into_db():
    load_csv_to_db(os.path.join(basedir, 'data', 'mouse_data_final.csv'), MouseReview)
    load_csv_to_db(os.path.join(basedir, 'data', 'monitor_final.csv'), MonitorReview)
    load_csv_to_db(os.path.join(basedir, 'data', 'headphone_final.csv'), HeadphoneReview)
    load_csv_to_db(os.path.join(basedir, 'data', 'Keyboard_final.csv'), KeyboardReview)

with app.app_context():
    inspector = inspect(db.engine)
    
    # Check if MouseReview table doesn't exist and create
    if not inspector.has_table(MouseReview.__tablename__):  
        MouseReview.__table__.create(bind=db.engine)
    
    # Check if MonitorReview table doesn't exist and create
    if not inspector.has_table(MonitorReview.__tablename__):  
        MonitorReview.__table__.create(bind=db.engine)

    # Check if HeadphoneReview table doesn't exist and create
    if not inspector.has_table(HeadphoneReview.__tablename__):  
        HeadphoneReview.__table__.create(bind=db.engine)
    # Check if KeyboardReview table doesn't exist and create
    if not inspector.has_table(KeyboardReview.__tablename__):  
        KeyboardReview.__table__.create(bind=db.engine)    

        
    load_data_into_db()  # Load data into both tables
    # ... (load other product CSVs similarly)

# ... (add more models for other products)

#@app.before_first_request

@app.route('/')
def index():
    return render_template('select_product.html')

PRODUCT_FEATURES = {
    'mouse': {
        'features': [
            "ergonomic_design",  # Comfortable for long-term use
            "adjustable_dpi",    # Change sensitivity/resolution
            "programmable_buttons", # Customize buttons for specific functions
            "wireless_connectivity", # No cords to tangle
            "long_battery_life", # Infrequent charging or battery changes
            "durable_build",    # Resistant to wear and tear
            "optical_sensor",   # Accurate tracking
            "scroll_wheel",     # Easy navigation on web pages/documents
            "ambidextrous",     # Suitable for both right and left-handed users
            "compact_size",     # Portable and doesn't occupy much space
             
             
            
        ],
        'keywords': {
            "ergonomic_design": ["comfortable", "ergonomic", "long-term use", "fits hand"],
            "adjustable_dpi": ["adjustable dpi", "sensitivity", "resolution", "change dpi"],
            "programmable_buttons": ["programmable button", "customize button", "specific function"],
            "wireless_connectivity": ["wireless", "no cord", "bluetooth", "connectivity"],
            "long_battery_life": ["long battery", "infrequent charging", "battery life", "battery lasts"],
            "durable_build": ["durable", "resistant", "wear and tear", "long lasting"],
            "optical_sensor": ["optical sensor", "accurate tracking", "sensor"],
            "scroll_wheel": ["scroll", "scrolling", "wheel", "navigate"],
            "ambidextrous": ["ambidextrous", "both hands", "right and left hand", "universal"],
            "compact_size": ["compact", "small size", "portable", "lightweight"]
           
        }
        
    },
    'monitor': {
        'features': [
            "high_resolution",     # Clear, detailed image quality
            "fast_refresh_rate",   # Smoother visuals, less motion blur
            "wide_viewing_angle",  # Clear images from different angles
            "color_accuracy",      # True-to-life colors
            "adjustable_stand",    # Ergonomics and comfort
            "thin_bezel",          # Modern look and optimal multi-monitor setup
            "built_in_speakers",   # Integrated audio
            "multiple_ports",      # Variety of connectivity options
            "low_blue_light",      # Eye comfort
            "energy_efficient",    # Low power consumption
            "size_range: 21-24",
            "size_range: 25-27",
            "size_range: 28-32",
            "size_range: 32-49"          
        ],
        'keywords': {
            "high_resolution": ["high resolution", "HD", "4K", "1080p", "clear image", "detailed", "QHD"],
            "fast_refresh_rate": ["fast refresh rate", "smooth visual", "less blur", "Hz", "high refresh rate"],
            "wide_viewing_angle": ["wide viewing angle", "clear from angle", "IPS", "viewing angle"],
            "color_accuracy": ["color accurate", "true-to-life", "sRGB", "color gamut"],
            "adjustable_stand": ["adjustable stand", "ergonomic", "height adjust", "tilt", "swivel"],
            "thin_bezel": ["thin bezel", "slim bezel", "modern look", "multi-monitor", "borderless"],
            "built_in_speakers": ["built-in speakers", "integrated audio", "speakers", "audio"],
            "multiple_ports": ["multiple ports", "HDMI", "USB-C", "DisplayPort", "connectivity"],
            "low_blue_light": ["low blue light", "eye comfort", "eye care", "blue light filter"],
            "energy_efficient": ["energy efficient", "low power", "eco mode", "power saving"],
            "size_range: 21-24":["21","22","23","24"],
            "size_range: 25-27":["25","26","27"],
            "size_range: 28-32":["28","29","30","31","32"],
            "size_range: 32-49":["32","34","49"]
        }
    },
    'headphones':{
    'features': [
        "noise_cancellation",         # Reduces external noise
        "wireless_connectivity",      # No cords to tangle
        "long_battery_life",          # Infrequent charging or battery changes
        "high_audio_quality",         # Clear, rich sound
        "comfortable_fit",            # Comfortable for long-term use
        "built_in_microphone",        # Integrated microphone for calls
        "durable_build",              # Resistant to wear and tear
        "foldable_design",            # Easy to store and transport
        "touch_controls",             # Easy control through touch gestures
        "quick_charge"                # Fast battery charging
    ],
    'keywords': {
        "noise_cancellation": ["noise cancellation", "noise cancelling", "ANC", "active noise"],
        "wireless_connectivity": ["wireless", "bluetooth", "no cords", "cordless"],
        "long_battery_life": ["long battery", "battery life", "long-lasting", "battery lasts"],
        "high_audio_quality": ["high audio", "clear sound", "rich sound", "audio quality"],
        "comfortable_fit": ["comfortable", "fits well", "soft ear", "comfort"],
        "built_in_microphone": ["built-in mic", "microphone", "calls", "voice"],
        "durable_build": ["durable", "long lasting", "wear and tear", "rugged"],
        "foldable_design": ["foldable", "folds", "compact", "portable"],
        "touch_controls": ["touch control", "gesture", "swipe", "touch"],
        "quick_charge": ["quick charge", "fast charge", "charge quickly", "rapid charge"]
    }
    },
    'keyboard':{
    'features': [
        "mechanical_keys",       # Tactile, audible key switches
        "rgb_lighting",          # Customizable backlighting
        "macro_keys",            # Programmable keys for custom commands
        "wireless_connectivity", # No cords to tangle
        "n_key_rollover",        # Allows multiple keys to be pressed at once
        "media_controls",        # Built-in media control keys or dials
        "ergonomic_design",      # Comfortable for long-term use
        "durable_build",         # Resistant to wear and tear
        "high_polling_rate",     # Faster input registration
        "palm_rest"              # Integrated or attachable palm rest
    ],
    'keywords': {
        "mechanical_keys": ["mechanical", "tactile", "audible", "switches"],
        "rgb_lighting": ["RGB", "backlighting", "customizable lighting", "LED"],
        "macro_keys": ["macro keys", "programmable", "custom commands"],
        "wireless_connectivity": ["wireless", "bluetooth", "no cords", "cordless"],
        "n_key_rollover": ["n-key rollover", "anti-ghosting", "multiple keys", "simultaneous keys"],
        "media_controls": ["media controls", "volume dial", "media keys", "play pause"],
        "ergonomic_design": ["ergonomic", "comfortable", "long-term use", "fits hand"],
        "durable_build": ["durable", "long-lasting", "resistant", "wear and tear"],
        "high_polling_rate": ["high polling rate", "fast input", "1000Hz", "polling rate"],
        "palm_rest": ["palm rest", "palm support"]
    }
    # ... (similar structures for other products like 'keyboard', 'headphone', etc.)
    },
}

@app.route('/product_details')
def product_details():
    product_category = request.args.get('product_category')
    features = PRODUCT_FEATURES.get(product_category, {}).get('features', [])
    return render_template('product_details.html', product_category=product_category, features=features)

PRODUCT_MODELS = {
    'mouse': MouseReview,
    'monitor': MonitorReview,
    'headphones': HeadphoneReview,
    'keyboard': KeyboardReview,
    
    # ... (add other product categories and their models)
}
def mentions_feature(text, feature_keywords):
    """
    Check if a given text mentions any of the keywords associated with a feature.
    """
    for keyword in feature_keywords:
        if keyword in text.lower():
            return True
    return False

def mentions_all_features(text, features_list, product_category):
    """
    Check if a given text mentions all the keywords associated with a list of features.
    """
    return all(mentions_feature(text, PRODUCT_FEATURES[product_category]['keywords'][feature]) for feature in features_list)

@app.route('/reviews')
def reviews():
    product_category = request.args.get('product_category')
    selected_features = request.args.getlist('feature')
    
    print(f"Selected features: {selected_features}")

    model = PRODUCT_MODELS.get(product_category)
    
    # Construct the filter conditions
    filters = []

    for feature in selected_features:
        keyword_filters = [model.review_content.ilike(f"%{keyword}%") for keyword in PRODUCT_FEATURES[product_category]['keywords'][feature]]
        filters.append(or_(*keyword_filters))

    print(f"Filters: {filters}")

    # Fetch reviews that match the conditions
    filtered_reviews = model.query.filter(and_(*filters)).order_by(model.positive_score.desc()).limit(5).all()

    print(f"Filtered reviews: {filtered_reviews}")

    return render_template('reviews_display.html', reviews=filtered_reviews, product_category=product_category)

if __name__ == '__main__':
    app.run(debug=True)

mkdir templates 
python3 scaffold.py country name
python3 scaffold.py user username email password country_id:references phone
python3 scaffold.py influencer_country_identity name identity_type  country_id:references
python3 scaffold.py copy_country_trend country_id:references influencer_country_identity_id:references
python3 scaffold.py socialmedia name
python3 scaffold.py carteajouer socialmedia_id:references title content user_id:references playingcard_name pic:file copy_country_trend_id:references

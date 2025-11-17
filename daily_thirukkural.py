import os
import smtplib
import ssl
from email.message import EmailMessage
import random 

# --- 1. CONFIGURATION (UPDATE THESE 3 LINES) ---
# Your sending Gmail address
# --- 1. CONFIGURATION (READ FROM GITHUB ACTIONS SECRETS) ---

APP_PASSWORD = os.environ.get("APP_PASSWORD") 
SENDER_EMAIL = os.environ.get("SENDER_EMAIL") 

RECEIVER_EMAILS_STR = os.environ.get(
    "RECEIVER_EMAILS", 
    "sabarimk.nagaraj@gmail.com,sabarinagaraj17@gmail.com" # Fallback list
) 

RECEIVER_EMAILS = [email.strip() for email in RECEIVER_EMAILS_STR.split(',')]
SENDER_DISPLAY_NAME = "திருவள்ளுவர்"

# --- 2. LOCAL DATA SOURCE (FIRST 50 THEMED KURALS) ---
# This list ensures 100% reliability, removing external API dependencies.
THIRUKKURAL_DATA = [
    # --- MOTIVATION/HARD WORK (ஊக்கமுடைமை) ---
    {
        "number": 591,
        "athigaram": "ஊக்கமுடைமை",
        "kural": "உள்ளம் உடைமை உடைமை பொருளுடைமை\nநில்லாது நீங்கி விடும்.",
        "tamil_meaning": "உள்ளத்து ஊக்கமே நிலையான உடைமையாகும். மற்றப் பொருட்செல்வமோ நிலைத்து நில்லாமல் நீங்கிப் போய்விடும்.",
        "english_meaning": "The possession of energy is real possession; the possession of wealth is a false possession, for it will not endure."
    },
    {
        "number": 594,
        "athigaram": "ஊக்கமுடைமை",
        "kural": "வெள்ளத்தனையது தாமரைப்பூம்; மாந்தர்தம்\nஉள்ளத் தனையது உயர்வு.",
        "tamil_meaning": "தாமரை மலரின் உயரம் அது வளர்ந்துள்ள நீரின் அளவேயாகும். அதுபோல, ஒருவருடைய வாழ்க்கையின் உயர்வும் அவரது உள்ளத்து ஊக்கத்தின் அளவேயாகும்.",
        "english_meaning": "The lotus flower blooms in proportion to the water's depth; so is the greatness of men proportional to their minds' energy."
    },
    {
        "number": 612,
        "athigaram": "வினைத்திறம்",
        "kural": "செயற்கை அருமை அறியினும் கைப்பொருள்\nசெல்லா விடத்துச் செயல்.",
        "tamil_meaning": "செயலின் அருமையை உணர்ந்தாலும், கையிலுள்ள பொருள்கள் குறையாமல் செய்யத் தக்க வழிகளை அறிந்து செய்ய வேண்டும்.",
        "english_meaning": "Though the difficulty of an undertaking is known, it must be started, when there is no other resort."
    },
    {
        "number": 619,
        "athigaram": "ஆள்வினையுடைமை",
        "kural": "தெய்வத்தால் ஆகா தெனினும் முயற்சிதன்\nமெய்வருத்தக் கூலி தரும்.",
        "tamil_meaning": "ஊழின் காரணத்தால் ஒரு செயல் வெற்றி பெறாவிட்டாலும், முயற்சிக்குக் கிடைத்த ஊதியமாக அச்செயல் முயற்சியை மேற்கொண்டவரின் உடல் உழைப்பிற்குக் கூலியைக் கொடுத்துவிடும்.",
        "english_meaning": "Though it be said that the result of an act is the result of fate, yet the labour of the body will yield its reward."
    },
    {
        "number": 620,
        "athigaram": "ஆள்வினையுடைமை",
        "kural": "முயற்சி திருவினை ஆக்கும்; முயற்றின்மை\nஇன்மை புகுத்தி விடும்.",
        "tamil_meaning": "முயற்சி செல்வத்தை உண்டாக்கும்; முயற்சியின்மை வறுமைக்குள் தள்ளிவிடும்.",
        "english_meaning": "Labor will produce wealth; idleness will introduce poverty."
    },
    # --- FRIENDSHIP (நட்பு) ---
    {
        "number": 781,
        "athigaram": "நட்பு",
        "kural": "நட்பிற்கு வீற்றிருக்கை யாதெனின் கொள்:\nஅற்றார் இவரென்று உலகு ஆவது.",
        "tamil_meaning": "நட்பிற்குரிய சிறந்த இருக்கை எதுவென்றால், இவன் நண்பன் என உலகம் போற்றும் நிலையே ஆகும்.",
        "english_meaning": "If it be asked, 'What is the seat of friendship?' It is where the world proclaims 'This is the man'."
    },
    {
        "number": 783,
        "athigaram": "நட்பு",
        "kural": "நட்பின் இலக்கணம் எனில்: பிறன்அணி\nநின்று துணைசெய்வது.",
        "tamil_meaning": "நட்பின் இலக்கணம் என்னவென்றால், ஒருவன் தவறு செய்யும்போது அவன்மீது கோபம்கொண்டு, அவனைத் திருத்தி, பின் அவனுக்கு உதவுவதே ஆகும்.",
        "english_meaning": "The characteristics of friendship are not laughing and talking, but standing by a friend in trouble."
    },
    {
        "number": 784,
        "athigaram": "நட்பு",
        "kural": "நகைவகைய ராகார் நண்பர்; பகைவர்\nநகுதக்கன செய்தல் இலர்.",
        "tamil_meaning": "நண்பர்கள் எப்போதும் சிரித்துப் பேசி மகிழ்வோர் அல்லர்; தவறு செய்யும்போதெல்லாம் சினந்து திருத்துபவரே ஆவார்.",
        "english_meaning": "Friends are not those who are accustomed to laugh and talk, but those who correct their friend when he errs."
    },
    {
        "number": 787,
        "athigaram": "நட்பு",
        "kural": "உடுக்கை இழந்தவன் கைபோல ஆங்கே\nஇடுக்கண் களைவதாம் நட்பு.",
        "tamil_meaning": "உடையில்லாதவன் கை உடனே சென்று ஆடையை இழுத்துச் சேர்ப்பதுபோல, நண்பனுக்கு வந்த துன்பத்தை உடனே நீக்குவதே நட்பாகும்.",
        "english_meaning": "Like the hand of one whose garment is displaced, friendship is the immediate help rendered to one in distress."
    },
    {
        "number": 788,
        "athigaram": "நட்பு",
        "kural": "அழிவின்மை வேண்டியவன் நட்பு வேண்டின்,\nசலியாமை வேண்டல் நன்று.",
        "tamil_meaning": "அழியாத நட்பை விரும்புபவன், நண்பன் துன்பத்தில் கலங்காமல் இருக்கவேண்டும் என்று விரும்புவது நன்று.",
        "english_meaning": "If a man desires friendship that cannot be injured, let him desire that he should not be weary of his friend's suffering."
    },
    # --- LOVE (காமத்துப்பால் - களவியல்) ---
    {
        "number": 1081,
        "athigaram": "கண்டார் கேட்டார்",
        "kural": "கண்டார் கேட்டார் எனக்கருதி காமுறார்\nபண்டே அவர்எனத் தொண்டுறாமை.",
        "tamil_meaning": "இவருடைய அழகைக் கண்டவர்கள்தான் இவரை விரும்புகிறார்கள் என்று எண்ணாமல், இவர் என்னுடையவர் என்று உரிமை கொண்டாடுதல்.",
        "english_meaning": "Do not regard him as one whom others have seen and fallen in love with; claim him as your own, saying, 'He is mine'."
    },
    {
        "number": 1103,
        "athigaram": "தகை அணங்குறுத்தல்",
        "kural": "அணங்குகொல் ஆய்மயிலோ என்றுகொண்டு\nஆயும்நம் பேதைதன் பெடை.",
        "tamil_meaning": "இவள் தெய்வப்பெண்ணோ அல்லது சிறந்த மயிலோ என எண்ணிப் பலரும் வியக்கும்படி விளங்குகிறாள், நம் பேதைப் பெண்.",
        "english_meaning": "Is she an angel, or a beautiful peacock? Thus do people wonder and praise the beauty of our innocent girl."
    },
    {
        "number": 1106,
        "athigaram": "தகை அணங்குறுத்தல்",
        "kural": "நோக்கினாற் தாக்கி நறுநதக்கிற் செல்லும்\nமழைகொலோ மற்றவர் கண்.",
        "tamil_meaning": "பார்வையால் என்னைத் தாக்கிவிட்டு, பின் புன்னகையால் என்னைச் சேருகின்ற அந்தப் பெண்ணின் கண்கள் மலர்களா? இல்லை, மழைத்துளியோ?",
        "english_meaning": "Are they flowers or drops of rain, those eyes which strike me with their look and then smile gently?"
    },
    {
        "number": 1107,
        "athigaram": "தகை அணங்குறுத்தல்",
        "kural": "கடவுளோ கொல் அன்றி கள்வர் கொல்\nஅற்றவர்கண் கொள்ளும் இவன்.",
        "tamil_meaning": "இவள் கடவுளோ அல்லது கள்வனோ? பிறர் கள்ளால் என் நெஞ்சைக் கவர்ந்தவர் இவள்.",
        "english_meaning": "Is she a Goddess or a thief? She steals my heart with her beautiful eyes."
    },
    {
        "number": 1111,
        "athigaram": "குறிப்பறிதல்",
        "kural": "இருநோக்கு இவள்உண்கண் உள்ளது; ஒருநோக்கு\nநோய்நோக்கு; மற்றுஓர் மருந்து.",
        "tamil_meaning": "இவளுடைய மையுண்ட கண்களில் இரண்டு வகையான நோக்கங்கள் உள்ளன; ஒரு நோக்கு நோய் செய்வது; மற்றொரு நோக்கு அந்நோய்க்கு மருந்தாவது.",
        "english_meaning": "There are two kinds of looks in this woman's painted eyes: one creates the sickness, the other is its medicine."
    },
    {
        "number": 1119,
        "athigaram": "புணர்ச்சி மகிழ்தல்",
        "kural": "நன்னீரை வாழி அனிச்சமே நின்னினும்\nமென்னீரள் யாம்வீழ் பவள்.",
        "tamil_meaning": "அனிச்ச மலரே! நீயும் வாழ்க! உன்னைவிட மென்மையானவள் நான் விரும்பும் என் தலைவி.",
        "english_meaning": "Live long, O Anicham flower! She whom I love is more delicate than you."
    },
    {
        "number": 1131,
        "athigaram": "நலம் புனைந்துரைத்தல்",
        "kural": "கண்ணின் கடைப்பார்வை காதலர்கண் டால்அவரை\nநண்ணுதல் இனிதெனல் நன்று.",
        "tamil_meaning": "காதலர் ஒருவரையொருவர் கண்டால், அவருடைய கண்ணின் கடைப்பார்வை பேசுவது இனிமையானது.",
        "english_meaning": "When lovers see each other, the casual glance of the eye is sweet."
    },
    {
        "number": 1133,
        "athigaram": "நலம் புனைந்துரைத்தல்",
        "kural": "உற்றார் அறிவுறும் கண்ணும் மறையினால்\nஇன்புறுதல் என்றும் இல.",
        "tamil_meaning": "உறவினர்கள் சூழ்ந்திருந்தாலும், காதலர்கள் ஒருவரையொருவர் மறைத்துக் கொள்ளும் பார்வை இன்பமானது.",
        "english_meaning": "Even when surrounded by others, the secret glances exchanged by lovers are delightful."
    },
    {
        "number": 1141,
        "athigaram": "நிறை அழிதல்",
        "kural": "காதலர் கையறக் கண்டால்; அவர்முகம்\nநோக்கலின் நன்மையின் ஓர்அருள்.",
        "tamil_meaning": "காதலர் முகம் வாடக் கண்டால், அது காதலியின் உள்ளத்தில் இரக்கத்தை உண்டாக்கும்.",
        "english_meaning": "When a lover sees the face of his beloved clouded, it creates compassion in the heart of the beloved."
    },
    {
        "number": 1145,
        "athigaram": "நிறை அழிதல்",
        "kural": "நெஞ்சத்த காதலர் புன்செயல் கண்டால்\nஉள்ளம் உவகை பெறும்.",
        "tamil_meaning": "மனதிற்குள் இருக்கும் காதலனின் சின்னச் சின்னச் செயல்களைக் கண்டால், உள்ளம் மகிழ்வடையும்.",
        "english_meaning": "When one sees the trifling deeds of the lover in the heart, the mind feels delighted."
    },
    # (Additional 30 Kurals focusing on your requested themes would be inserted here for a total of 50)
    # Placeholder for the rest of the 50 themed Kurals
] 
# ----------------------------------------------------------------------------------

def get_local_kural():
    """Picks one random Kural from the local list."""
    if not THIRUKKURAL_DATA:
        print("Error: Thirukkural data list is empty.")
        return None, None, None, None, None
        
    kural_data = random.choice(THIRUKKURAL_DATA)
    
    # Extract data using the guaranteed keys from the local list
    tamil_text = kural_data.get("kural", "Tamil text missing.")
    translation_en = kural_data.get("english_meaning", "English meaning missing.")
    translation_ta = kural_data.get("tamil_meaning", "Tamil meaning missing.")
    kural_num = kural_data.get("number", "Unknown")
    athigaram = kural_data.get("athigaram", "Unknown")
    
    return tamil_text, translation_en, translation_ta, kural_num, athigaram

def send_daily_kural():
    tamil_text, translation_en, translation_ta, kural_num, athigaram = get_local_kural()
    
    if kural_num == "Unknown":
        print("Script aborted due to missing local data.")
        return 

    # 💥 CRUCIAL FIX: Convert Python line break (\n) to HTML break (<br>) 
    # to maintain the 4-word/3-word Kural structure in the email body.
    formatted_tamil_text = tamil_text.replace('\n', '<br>') 
    # ------------------------------------------------------------------

    # --- HTML BODY WITH ANCIENT MANUSCRIPT THEME AND 3 IMAGES ---
    subject = f"📜 இன்றைய குறள் : குறள்: {kural_num} ({athigaram})"
    
    THIRUVALLUVAR_IMAGE_URL = "https://wallpaperaccess.com/full/8298424.jpg"
    DUMMY_PIC_1_URL = "https://i.pinimg.com/736x/99/61/36/996136a055f3cbbba0c0b1274fe502ae.jpg" 
    DUMMY_PIC_2_URL = "https://cdn.shopify.com/s/files/1/1284/2827/products/Prabhakaran142_1024x1024.jpg?v=1608783481" 
    
    PARCHMENT_COLOR = "#F8F8F0" 
    BROWN_BORDER = "#8B4513"

    html_body = f"""
    <html>
        <body style="font-family: 'Times New Roman', serif; 
                     line-height: 1.6; /* Reduced line height */
                     color: #333333; 
                     background-color: {PARCHMENT_COLOR}; 
                     padding: 20px; /* Reduced padding */
                     border: 2px solid {BROWN_BORDER}; 
                     max-width: 600px; 
                     margin: auto;">
            
            <div style="float: right; margin: 0 0 15px 15px; display: flex; align-items: flex-end;">
                
                <img 
                    src="{DUMMY_PIC_1_URL}" 
                    alt="Small Picture 1" 
                    style="width: 35px; height: 35px; border: 1px solid #5C4033; margin-right: 5px; opacity: 0.9;"
                >
                
                <img 
                    src="{DUMMY_PIC_2_URL}" 
                    alt="Small Picture 2" 
                    style="width: 35px; height: 35px; border: 1px solid #5C4033; margin-right: 5px; opacity: 0.9;"
                >

                <img 
                    src="{THIRUVALLUVAR_IMAGE_URL}" 
                    alt="Thiruvalluvar Image" 
                    style="width: 80px; height: 80px; border-radius: 5px; border: 1px solid #5C4033; opacity: 0.9;"
                >
            </div>
            <p style="color: #5C4033; font-size: 16px; font-weight: bold; margin-bottom: 15px;">
                நண்பா! உனது நாள் இனிய நாளாய் மலர இதோ இன்றைக்கான வள்ளுவனின் வாய்ச்சொல்
            </p>
            
            <hr style="border: none; border-top: 1px dashed #5C4033; margin: 15px 0;">
            
            <table style="width: 100%; margin-bottom: 15px;">
    <tr>
        <td style="width: 50%; color: #5C4033; font-weight: bold; font-size: 14px; white-space: nowrap; padding-right: 5px;">
            திருக்குறள் (Kural): {kural_num}
        </td>
        <td style="width: 50%; color: #5C4033; text-align: right; font-weight: bold; font-size: 14px; white-space: nowrap; padding-left: 5px;">
            அதிகாரம் (Chapter): {athigaram}
        </td>
    </tr>
</table>

<p style="font-size: 20px; /* Reduced font size for better fit */
          color: #000000;
          margin-top: 20px;
          margin-bottom: 20px;
          text-align: center; /* Centered for better mobile look */
          line-height: 1.2;
          padding: 5px 0;">
    <strong style="color: #444444;">குறள்:</strong><br>
    {formatted_tamil_text} 
</p>
            <h3 style="color: #5C4033; border-bottom: 1px dashed #5C4033; padding-bottom: 5px; margin-top: 15px; margin-bottom: 10px;">பொருள்:</h3>
            <p style="font-style: italic; color: #444444; margin-bottom: 15px;">
                {translation_ta}
            </p>

            <h3 style="color: #5C4033; border-bottom: 1px dashed #5C4033; padding-bottom: 5px; margin-top: 15px; margin-bottom: 10px;">Meaning:</h3>
            <p style="font-style: italic; color: #444444; margin-bottom: 20px;">
                {translation_en}
            </p>
            
            <hr style="border: none; border-top: 1px dashed #5C4033; margin: 15px 0;">
            
            <p style="text-align: center; font-size: 18px; font-weight: bold; color: #8B0000; margin-top: 15px;">
                உறுதியுடன் இன்றை உனதாக்கு நாளை உனதே!
            </p>
            
            <p style="font-size: 14px; margin-top: 20px; border-top: 1px dashed #5C4033; padding-top: 10px;">
                <span style="color: #5C4033; font-weight: bold;">வாழ்க தமிழ்!</span> 
                <span style="float: right; color: #5C4033; font-weight: bold;">வளர்க தமிழர்!</span>
            </p>
            
            <p style="font-size: 13px; margin-top: 10px; text-align: right;">
                இவண்<br>
                <strong style="color: #5C4033;">தமிழர் வாழ்வியல் இயக்கம்</strong>
            </p>
        </body>
    </html>
    """
    # ... rest of the send_daily_kural function remains the same ...
    
    # ... rest of the send_daily_kural function remains the same ...
    # ----------------------------------------
    
    # 3. Setup Email Headers and Content
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f"{SENDER_DISPLAY_NAME} <{SENDER_EMAIL}>" 
    msg['To'] = ", ".join(RECEIVER_EMAILS)
    msg.set_content(html_body, subtype='html') 
    
    context = ssl.create_default_context()
    
    # 4. Setup Secure Connection and Send
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            print("Successfully logged into Gmail.")
            
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())
            
            print(f"Sent Kural #{kural_num} ({athigaram}) to {len(RECEIVER_EMAILS)} recipient(s).")

    except Exception as e:
        print(f"A critical error occurred during email transmission: {e}")

if __name__ == "__main__":

    send_daily_kural()


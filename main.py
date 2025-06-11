import telebot
import requests
import json

# Hardcoded bot token
BOT_TOKEN = "7695862437:AAHpZbX-i1BxwHEEtxrQebL3pz8DilIFBLw"

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Aadhaar API details
AADHAAR_API_URL = "https://kyc-api.aadhaarkyc.io/api/v1/aadhaar-validation/aadhaar-validation"
AADHAAR_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTIxNDczNSwianRpIjoiMmE4MWZkMTUtNWU0Yy00NjY1LWE0NTItYTE4ZDRmZTRkOTdkIiwidHlwZSI6ImFjY2VzcyIsImlkZW50aXR5IjoiZGV2LmtyNGFsbEBhYWRoYWFyYXBpLmlvIiwibmJmIjoxNjQxMjE0NzM1LCJleHAiOjE5NTY1NzQ3MzUsInVzZXJfY2xhaW1zIjp7InNjb3BlcyI6WyJyZWFkIl19fQ.xq-191hmb69EjYkJ5r4c2yAJNf2lMqnA_3PhfnCrzNY"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Aadhaar Validation Bot! Send me an Aadhaar number to validate.")

@bot.message_handler(func=lambda message: True)
def validate_aadhaar(message):
    aadhaar_number = message.text.strip()
    
    # Basic validation for 12 digits
    if not (aadhaar_number.isdigit() and len(aadhaar_number) == 12):
        bot.reply_to(message, "Please send a valid 12-digit Aadhaar number.")
        return
    
    # Call the Aadhaar validation API
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {AADHAAR_API_KEY}'
        }
        
        payload = json.dumps({
            "id_number": aadhaar_number
        })
        
        response = requests.post(AADHAAR_API_URL, headers=headers, data=payload)
        result = response.json()
        
        # Format the response as per requirements
        if result.get('success') == True:
            formatted_response = f"""
✅ Validation Successful!

📋 Details:
- Aadhaar Number: {result['data']['aadhaar_number']}
- State: {result['data']['state']}
- Gender: {result['data']['gender']}
- Age Range: {result['data']['age_range']}
- Mobile Linked: {'Yes' if result['data']['is_mobile'] else 'No'}
- Last Digits: {result['data']['last_digits']}
    Credit @icodeinbinary
            """
            bot.reply_to(message, formatted_response)
        else:
            bot.reply_to(message, f"❌ Validation Failed: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("Bot started...")
    bot.polling() 

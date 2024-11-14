import csv
import json
import pandas as pd

# Read the construction materials dataset (CSV file)
materials = []
df = pd.read_csv('dataset.csv', encoding='utf-8')
df.columns = df.columns.str.strip()

# Convert the dataframe into a list of dictionaries
materials = df.to_dict(orient='records')

# Structure the intents.json
intents = {"intents": []}

# Add general conversational intents (greetings, goodbye, thanks, etc.)
intents["intents"].extend([
    {
        "tag": "greeting",
        "patterns": ["Hi", "Hello", "Hey", "Hi there", "Hello there", "Hey there", "Greetings", "What's up?", "Good morning", "Good afternoon"],
        "responses": ["Hello! How can I assist you with construction material information?", "Hi there! Looking for material pricing or help with construction materials?", "Hello! How can I help you today?", "Hi! What can I help you with today?"],
        "context": [""]
    },
    {
        "tag": "goodbye",
        "patterns": ["Bye", "Goodbye", "See you later", "Talk to you later", "Catch you later", "I’m out", "Goodbye for now", "Bye-bye", "Take care", "Later!"],
        "responses": ["Goodbye! Feel free to ask anytime!", "See you later!", "Goodbye! I'm here if you need anything else.", "Take care, and talk to you soon!"],
        "context": [""]
    },
    {
        "tag": "thanks",
        "patterns": ["Thanks", "Thank you", "I appreciate it", "Thanks a lot", "Much appreciated", "Thank you very much", "I am grateful", "That was helpful", "Thanks for your help", "Thanks a million"],
        "responses": ["You're welcome!", "Glad to help!", "You're welcome! Let me know if you need more assistance.", "Anytime! Feel free to ask if you have more questions."],
        "context": [""]
    },
    {
        "tag": "options",
        "patterns": ["What can you do?", "How can you help me?", "What support do you offer?", "What services are available?", "How can you assist me?", "What features are available?", "What services do you provide?", "What can I use here?", "What tools do you have?", "How can you assist with construction materials?"],
        "responses": ["I can provide cost estimates for construction materials, material descriptions, and more. Just ask!", "I can help you calculate material costs, find descriptions of materials, and guide you with construction material suggestions.", "I offer material pricing information, cost calculations, and recommendations.", "I can assist with cost estimates, material descriptions, and construction material recommendations. Just let me know what you need."],
        "context": [""]
    }
])

# Add material-related intents (for cost and description queries)
for material in materials:
    material_name = material["Material_Name"].strip().lower()

    # Intent to query material cost
    intents["intents"].append({
        "tag": f"{material_name}_cost",
        "patterns": [f"How much does {material['Material_Name']} cost?", f"What is the price of {material['Material_Name']}?", f"Cost of {material['Material_Name']}", f"Price of {material['Material_Name']}", f"How much for {material['Material_Name']}?", f"Tell me the cost of {material['Material_Name']}", f"What's the price for {material['Material_Name']}?", f"How much does one {material['Material_Name']} cost?", f"Can you give me the price for {material['Material_Name']}?", f"Is {material['Material_Name']} expensive?"],
        "responses": [f"The cost of {material['Material_Name']} is {material['Cost Price']} {material['Currency']} per unit. How many units would you like to know the total price for?"],
        "context": [""]
    })

    # Intent to query material description
    intents["intents"].append({
        "tag": f"{material_name}_description",
        "patterns": [f"Tell me about {material['Material_Name']}", f"Description of {material['Material_Name']}", f"What is {material['Material_Name']}?", f"Describe {material['Material_Name']}", f"What's {material['Material_Name']} used for?", f"Can you describe {material['Material_Name']}?", f"Give me details about {material['Material_Name']}", f"What can you tell me about {material['Material_Name']}?", f"What's {material['Material_Name']}?", f"How do I use {material['Material_Name']}?"],
        "responses": [f"{material['Material_Name']} is described as: {material['Description']}."],
        "context": [""]
    })

# Handle calculation-related intents by prompting users to use the calculator
calculation_intents = [
    {
        "tag": "cost_for_units",
        "patterns": ["What is the total cost for 100 bricks?", "How much for 50 blocks?", "How much does 200 tiles cost?", "Can you calculate the cost for 100 bricks?", "What is the price for 50 tiles?", "How much for 500 bricks?", "Can you tell me the total price for 100 tiles?", "What is the total cost for 50 panels?", "How much would it be for 200 bricks?", "What's the price for 50 units of tiles?"],
        "responses": ["Please use the calculator to get the total cost of materials. You can ask for the unit price and use the calculator.", "To calculate total costs, please use the calculator tool.", "You can use the cost calculator to find the total price for your materials."],
        "context": [""]
    },
    {
        "tag": "paint_calculation",
        "patterns": ["How much paint do I need for a wall of 10 meters by 5 meters?", "How many liters of paint for a 10m x 5m wall?", "What paint amount do I need?", "Can you calculate the paint for a 12m wall?", "How much paint is required for a room?", "How many liters of paint for 5 meters by 5 meters?", "How much paint for a 15m by 10m wall?", "Tell me how much paint I need", "Calculate paint for a wall", "What is the paint quantity for a 6m wall?"],
        "responses": ["Please use the paint calculator tool to calculate the required amount of paint for your wall dimensions.", "You can calculate paint requirements using the paint calculator on our website.", "Please use the calculator tool to find out how much paint you need based on your wall size."],
        "context": [""]
    },
    {
        "tag": "tile_cost_calculation",
        "patterns": ["Can I calculate the cost for tiles?", "How do I calculate the cost of tiles for my project?", "What's the cost for tiling a room?", "How can I calculate tile costs?", "Can you help me calculate tile costs?", "How much for tiling a 10m x 5m room?", "Can I calculate tile prices?", "Can you tell me how to calculate tile costs?", "Help me calculate tile costs for my project", "What's the tile price calculation?"],
        "responses": ["Please use the tile calculator to calculate costs for your tiling project.", "You can use the tile cost calculator tool to get the total cost for tiles.", "Please use the calculator to get an estimate for the tile cost."],
        "context": [""]
    }
]

intents["intents"].extend(calculation_intents)

# Add new intents for app and company info
intents["intents"].extend([
    {
        "tag": "website_help",
        "patterns": ["What can this website help me with?", "How does this website work?", "What is the purpose of this website?", "Can you tell me what this website does?", "How does your site help?", "What services does this website offer?", "What can I do on this platform?", "How can this platform help me?", "What's the purpose of this platform?", "How can I use this site?"],
        "responses": ["This website helps you calculate the material quantities and costs needed for your construction projects.", "You can use this website to calculate material costs and quantities for construction projects.", "This platform assists with calculating costs and materials for construction projects.", "The website is designed to help you calculate costs for materials like bricks, paint, tiles, and more."],
        "context": [""]
    },
    {
        "tag": "contact_support",
        "patterns": ["How can I contact support?", "What is your support email?", "How do I reach out to support?", "Can I contact customer service?", "How do I get help?", "What's your support number?", "What is your customer service phone number?", "Can you give me your support email?", "How do I contact customer service?", "What is the support contact information?"],
        "responses": ["You can reach out to support by sending an email to support@mcc.com or calling us at 971552265107.", "To contact support, send an email to support@mcc.com or call 971552265107.", "Feel free to contact us via email at support@mcc.com or call us at 971552265107.", "Our support team is available at support@mcc.com or by phone at 971552265107."],
        "context": [""]
    },
    {
        "tag": "available_tools",
        "patterns": ["What are the available tools on this platform?", "What tools do you offer?", "What calculators are available?", "What features do you have?", "Can you tell me the available tools?", "What tools can I use here?", "What calculators does the site have?", "Tell me the available tools", "What are the tools on this site?", "Can you list the available calculators?"],
        "responses": ["We have calculators for bricks, paint, lofts, and tiles, along with a cost calculator and material suggestions feature.", "Our platform offers calculators for bricks, paint, lofts, tiles, and more.", "You can use tools like the brick calculator, paint calculator, and cost calculator on this platform.", "We provide a variety of tools including calculators for paint, bricks, lofts, tiles, and more."],
        "context": [""]
    },
    {
        "tag": "guide_calculators",
        "patterns": ["Can you guide me on how to use the calculators?", "How do I use the calculators?", "How can I calculate material costs?", "Can you tell me how to use the calculators?", "I need help using the calculators", "How do I operate the calculators?", "Guide me through the calculators", "What are the steps to use the calculators?", "Can you help me with the calculators?", "Tell me how to use the calculators"],
        "responses": ["Sure! Just select a calculator from the menu, enter the required measurements, and click ‘Calculate’ to get your results.", "To use the calculators, choose the one you need, input your dimensions, and click 'Calculate'.", "Just pick the right calculator, enter your measurements, and get the results instantly.", "It's simple! Choose a calculator, input your dimensions, and hit ‘Calculate’ to get your material or cost estimate."],
        "context": [""]
    }
])

# Save the intents to a JSON file
with open('../modal/intents.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(intents, jsonfile, ensure_ascii=False, indent=4)

print("intents.json file created for construction materials and app info")

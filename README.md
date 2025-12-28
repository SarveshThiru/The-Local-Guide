# The Local Guide - Chennai Edition

A Kiro-powered local knowledge system that understands Chennai culture, Tamil slang, food, and traffic patterns through multiple interfaces.

## 🏛️ Features

- **Tamil Slang Translation**: Decode Chennai expressions like "machan", "semma", and "vera level"
- **Food Recommendations**: Discover authentic South Indian cuisine from crispy dosas to filter coffee
- **Traffic Intelligence**: Navigate Chennai's busy roads with OMR insights and monsoon considerations
- **Weather & Monsoon Wisdom**: Understand seasons from scorching summers to heavy rains
- **Cultural Insights**: Learn Tamil etiquette, festivals, and local attitudes

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Modern web browser
- Kiro IDE (optional, for enhanced development experience)

### Running the CLI Tool
```bash
python local_guide.py
```

Available commands:
- `translate <text>` - Translate Tamil/local slang
- `food [preference]` - Get food recommendations  
- `traffic [location]` - Check traffic conditions
- `insight <topic>` - Get local insights

### Running the Web Interface
Simply open `index.html` in your browser for an interactive web experience.

## 📁 Project Structure

```
├── .kiro/                  # Kiro configuration and steering
│   └── steering/
│       └── project-context.md
├── product.md              # Complete local knowledge base
├── local_guide.py          # Interactive CLI tool
├── index.html          # Web interface
└── README.md              # This file
```

## 🎯 Usage Examples

### CLI Examples
```bash
# Translate Tamil slang
translate "That's semma machan"

# Get food recommendations
food street food

# Check traffic conditions
traffic OMR

# Get monsoon insights
insight monsoon season
```

### Web Interface
Open `index.html` and try:
- Select "Translate Slang" and enter: "semma machan"
- Select "Food Recommendations" and enter: "filter coffee"
- Select "Traffic Conditions" and enter: "OMR traffic"

## 🧠 How It Works

The system uses `product.md` as a single source of truth containing comprehensive Chennai local knowledge. The Python CLI tool dynamically parses this markdown content to provide intelligent responses, while the web interface offers a user-friendly way to access the same information.

## 🛠️ Development with Kiro

This project includes Kiro steering files in `.kiro/steering/` that provide context about the project structure and development guidelines. When working with Kiro:

1. The steering context automatically guides development decisions
2. Maintains Chennai authenticity and respects Tamil culture
3. Keeps `product.md` as the authoritative knowledge source
4. Ensures consistent behavior across CLI and web interfaces

## 📝 Contributing

When adding new local knowledge:
1. Update `product.md` with new information
2. The CLI tool will automatically parse and use the new content
3. Update web interface JavaScript if needed for new features
4. Test both interfaces to ensure consistency

## 🌟 Local Authenticity

This guide maintains authentic Chennai perspective:
- Uses proper Tamil expressions and respectful addresses
- Includes real traffic patterns and monsoon considerations
- Reflects genuine local culture and food traditions
- Provides practical, insider knowledge for locals and visitors

## 🎭 Cultural Respect

- Respects Tamil language and culture
- Uses appropriate greetings like "Vanakkam"
- Acknowledges local customs and etiquette
- Celebrates Chennai's rich heritage and modern IT identity

---

*Built with ❤️ for Chennai locals and visitors who want the real inside scoop*
*வணக்கம் Chennai! (Vanakkam Chennai!)*
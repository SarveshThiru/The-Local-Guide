#!/usr/bin/env python3
"""
The Local Guide - Chennai Edition
A tool that understands local nuances through custom context
"""

import re
import json
from datetime import datetime, time
from typing import Dict, List, Optional, Tuple

class LocalGuide:
    def __init__(self, context_file: str = "product.md"):
        """Initialize the Local Guide with context from product.md"""
        self.context = self._load_context(context_file)
        self.slang_dict = self._parse_slang()
        self.food_spots = self._parse_food_spots()
        self.traffic_patterns = self._parse_traffic_patterns()
        
    def _load_context(self, filename: str) -> str:
        """Load the local context from product.md"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "Context file not found. Please ensure product.md exists."
    
    def _parse_slang(self) -> Dict[str, str]:
        """Extract slang dictionary from context"""
        slang = {}
        slang_section = re.search(r'## Local Slang & Expressions(.*?)##', self.context, re.DOTALL)
        if slang_section:
            lines = slang_section.group(1).strip().split('\n')
            for line in lines:
                if line.startswith('- **'):
                    match = re.match(r'- \*\*"?([^"*]+)"?\*\* - (.+)', line)
                    if match:
                        term, definition = match.groups()
                        slang[term.lower()] = definition
        return slang
    
    def _parse_food_spots(self) -> Dict[str, List[str]]:
        """Extract food recommendations from context"""
        foods = {"must_try": [], "spots": []}
        
        # Parse must-try foods
        must_try_section = re.search(r'### Must-Try Local Foods(.*?)### Popular Street Food Spots', self.context, re.DOTALL)
        if must_try_section:
            lines = must_try_section.group(1).strip().split('\n')
            for line in lines:
                if line.startswith('- **'):
                    match = re.match(r'- \*\*([^*]+)\*\* - (.+)', line)
                    if match:
                        food, description = match.groups()
                        foods["must_try"].append(f"{food}: {description}")
        
        # Parse food spots
        spots_section = re.search(r'### Popular Street Food Spots(.*?)## Traffic', self.context, re.DOTALL)
        if spots_section:
            lines = spots_section.group(1).strip().split('\n')
            for line in lines:
                if line.startswith('- **'):
                    match = re.match(r'- \*\*([^*]+)\*\* - (.+)', line)
                    if match:
                        area, description = match.groups()
                        foods["spots"].append(f"{area}: {description}")
        
        return foods
    
    def _parse_traffic_patterns(self) -> Dict[str, List[str]]:
        """Extract traffic information from context"""
        traffic = {"peak_hours": [], "hotspots": [], "tips": []}
        
        # Parse peak hours
        peak_section = re.search(r'### Peak Hours(.*?)### Traffic Hotspots', self.context, re.DOTALL)
        if peak_section:
            lines = peak_section.group(1).strip().split('\n')
            for line in lines:
                if line.startswith('- **'):
                    traffic["peak_hours"].append(line[3:])
        
        # Parse hotspots
        hotspots_section = re.search(r'### Traffic Hotspots to Avoid(.*?)### Local Transportation Tips', self.context, re.DOTALL)
        if hotspots_section:
            lines = hotspots_section.group(1).strip().split('\n')
            for line in lines:
                if line.startswith('- **'):
                    traffic["hotspots"].append(line[3:])
        
        # Parse tips
        tips_section = re.search(r'### Local Transportation Tips(.*?)## Weather', self.context, re.DOTALL)
        if tips_section:
            lines = tips_section.group(1).strip().split('\n')
            for line in lines:
                if line.startswith('- **'):
                    traffic["tips"].append(line[3:])
        
        return traffic

    def translate_slang(self, text: str) -> str:
        """Translate local slang in the given text"""
        result = []
        words = text.lower().split()
        
        for word in words:
            # Remove punctuation for matching
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word in self.slang_dict:
                result.append(f"'{word}' = {self.slang_dict[clean_word]}")
            else:
                # Check for partial matches
                for slang_term in self.slang_dict:
                    if slang_term in clean_word or clean_word in slang_term:
                        result.append(f"'{word}' (contains '{slang_term}') = {self.slang_dict[slang_term]}")
                        break
        
        if result:
            return "Slang translations found:\n" + "\n".join(result)
        else:
            return "No local slang detected in your text."

    def recommend_food(self, preference: str = "") -> str:
        """Recommend local food based on preference"""
        recommendations = []
        
        if "street" in preference.lower() or "quick" in preference.lower():
            recommendations.append("🌮 Street Food Recommendations:")
            recommendations.extend([f"  • {spot}" for spot in self.food_spots["spots"]])
        else:
            recommendations.append("🍽️ Must-Try Local Foods:")
            recommendations.extend([f"  • {food}" for food in self.food_spots["must_try"]])
        
        return "\n".join(recommendations)

    def estimate_traffic(self, location: str = "", current_time: Optional[datetime] = None) -> str:
        """Estimate traffic conditions"""
        if current_time is None:
            current_time = datetime.now()
        
        hour = current_time.hour
        day_of_week = current_time.weekday()  # 0 = Monday, 6 = Sunday
        
        traffic_level = "Light"
        advice = []
        
        # Check if it's rush hour
        if (7 <= hour <= 9) or (16 <= hour <= 19):
            if day_of_week < 5:  # Weekday
                traffic_level = "Heavy"
                advice.append("🚨 Rush hour traffic - expect delays")
        
        # Friday afternoon special case
        if day_of_week == 4 and 15 <= hour <= 20:
            traffic_level = "Very Heavy"
            advice.append("🚨 Friday afternoon - bridge traffic to suburbs")
        
        # Location-specific advice
        location_lower = location.lower()
        for hotspot in self.traffic_patterns["hotspots"]:
            hotspot_name = hotspot.split("**")[1].split("**")[0].lower()
            if hotspot_name in location_lower:
                advice.append(f"⚠️ {hotspot}")
        
        result = [f"🚦 Traffic Level: {traffic_level}"]
        if advice:
            result.extend(advice)
        
        result.append("\n📋 Transportation Tips:")
        result.extend([f"  • {tip}" for tip in self.traffic_patterns["tips"]])
        
        return "\n".join(result)

    def get_local_insight(self, query: str) -> str:
        """Get general local insights based on query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["weather", "climate", "fog", "temperature"]):
            return self._get_weather_info()
        elif any(word in query_lower for word in ["culture", "etiquette", "attitude", "local"]):
            return self._get_cultural_info()
        elif any(word in query_lower for word in ["emergency", "safety", "earthquake", "practical"]):
            return self._get_emergency_info()
        else:
            return "Ask me about: slang translation, food recommendations, traffic conditions, weather, culture, or emergency info!"
    
    def _get_weather_info(self) -> str:
        """Extract weather information"""
        weather_section = re.search(r'## Weather Microclimates(.*?)## Cultural', self.context, re.DOTALL)
        if weather_section:
            return "🌤️ SF Weather Microclimates:\n" + weather_section.group(1).strip()
        return "Weather information not available."
    
    def _get_cultural_info(self) -> str:
        """Extract cultural information"""
        culture_section = re.search(r'## Cultural Nuances(.*?)## Emergency', self.context, re.DOTALL)
        if culture_section:
            return "🏛️ Cultural Nuances:\n" + culture_section.group(1).strip()
        return "Cultural information not available."
    
    def _get_emergency_info(self) -> str:
        """Extract emergency information"""
        emergency_section = re.search(r'## Emergency & Practical Info(.*?)$', self.context, re.DOTALL)
        if emergency_section:
            return "🚨 Emergency & Practical Info:\n" + emergency_section.group(1).strip()
        return "Emergency information not available."


def main():
    """Interactive Local Guide CLI"""
    guide = LocalGuide()
    
    print("🏛️ Welcome to The Local Guide - Chennai Edition!")
    print("I understand Chennai culture, Tamil slang, food, and traffic patterns.")
    print("\nAvailable commands:")
    print("  translate <text>     - Translate local slang")
    print("  food [preference]    - Get food recommendations")
    print("  traffic [location]   - Check traffic conditions")
    print("  insight <topic>      - Get local insights")
    print("  help                 - Show this help")
    print("  quit                 - Exit the guide")
    
    while True:
        try:
            user_input = input("\n🗺️ Local Guide> ").strip()
            
            if not user_input or user_input.lower() == 'quit':
                print("Thanks for using The Local Guide! Vanakkam! 🏛️")
                break
            
            if user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  translate <text>     - Translate local slang")
                print("  food [preference]    - Get food recommendations") 
                print("  traffic [location]   - Check traffic conditions")
                print("  insight <topic>      - Get local insights")
                continue
            
            parts = user_input.split(' ', 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            if command == 'translate':
                if args:
                    print(guide.translate_slang(args))
                else:
                    print("Please provide text to translate. Example: translate 'That's semma machan'")
            
            elif command == 'food':
                print(guide.recommend_food(args))
            
            elif command == 'traffic':
                print(guide.estimate_traffic(args))
            
            elif command == 'insight':
                if args:
                    print(guide.get_local_insight(args))
                else:
                    print("Please specify a topic. Example: insight monsoon")
            
            else:
                print("Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\nThanks for using The Local Guide! 🏛️")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
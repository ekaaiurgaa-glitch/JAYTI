from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BirthChart, PlanetPosition, HouseDetail, Prediction
from datetime import datetime, timedelta
import swisseph as swe
import math

# Jayti's birth data
JAYTI_BIRTH_DATA = {
    'year': 1997,
    'month': 2,
    'day': 6,
    'hour': 22,
    'minute': 30,
    'latitude': 28.61,
    'longitude': 77.21,
    'timezone': 'Asia/Kolkata',
    'location': 'Delhi, India',
}

# Vedic Astrology Constants
PLANETS = {
    swe.SUN: ('sun', 'Sun', '☉'),
    swe.MOON: ('moon', 'Moon', '☽'),
    swe.MARS: ('mars', 'Mars', '♂'),
    swe.MERCURY: ('mercury', 'Mercury', '☿'),
    swe.JUPITER: ('jupiter', 'Jupiter', '♃'),
    swe.VENUS: ('venus', 'Venus', '♀'),
    swe.SATURN: ('saturn', 'Saturn', '♄'),
    swe.TRUE_NODE: ('rahu', 'Rahu', '☊'),
}

# Calculate Ketu position (opposite to Rahu)
def get_ketu_position(rahu_degree):
    """Ketu is always 180 degrees opposite to Rahu"""
    ketu_degree = (rahu_degree + 180) % 360
    return ketu_degree

RASHIS = [
    ('aries', 'Aries (Mesha)', 0, '♈'),
    ('taurus', 'Taurus (Vrishabha)', 30, '♉'),
    ('gemini', 'Gemini (Mithuna)', 60, '♊'),
    ('cancer', 'Cancer (Karka)', 90, '♋'),
    ('leo', 'Leo (Simha)', 120, '♌'),
    ('virgo', 'Virgo (Kanya)', 150, '♍'),
    ('libra', 'Libra (Tula)', 180, '♎'),
    ('scorpio', 'Scorpio (Vrishchika)', 210, '♏'),
    ('sagittarius', 'Sagittarius (Dhanu)', 240, '♐'),
    ('capricorn', 'Capricorn (Makara)', 270, '♑'),
    ('aquarius', 'Aquarius (Kumbha)', 300, '♒'),
    ('pisces', 'Pisces (Meena)', 330, '♓'),
]

NAKSHATRAS = [
    ('Ashwini', 0, 'Ketu'),
    ('Bharani', 13.33, 'Venus'),
    ('Krittika', 26.66, 'Sun'),
    ('Rohini', 40, 'Moon'),
    ('Mrigashira', 53.33, 'Mars'),
    ('Ardra', 66.66, 'Rahu'),
    ('Punarvasu', 80, 'Jupiter'),
    ('Pushya', 93.33, 'Saturn'),
    ('Ashlesha', 106.66, 'Mercury'),
    ('Magha', 120, 'Ketu'),
    ('Purva Phalguni', 133.33, 'Venus'),
    ('Uttara Phalguni', 146.66, 'Sun'),
    ('Hasta', 160, 'Moon'),
    ('Chitra', 173.33, 'Mars'),
    ('Swati', 186.66, 'Rahu'),
    ('Vishakha', 200, 'Jupiter'),
    ('Anuradha', 213.33, 'Saturn'),
    ('Jyeshtha', 226.66, 'Mercury'),
    ('Mula', 240, 'Ketu'),
    ('Purva Ashadha', 253.33, 'Venus'),
    ('Uttara Ashadha', 266.66, 'Sun'),
    ('Shravana', 280, 'Moon'),
    ('Dhanishta', 293.33, 'Mars'),
    ('Shatabhisha', 306.66, 'Rahu'),
    ('Purva Bhadrapada', 320, 'Jupiter'),
    ('Uttara Bhadrapada', 333.33, 'Saturn'),
    ('Revati', 346.66, 'Mercury'),
]

RASHI_INFO = {
    'aries': {'element': 'Fire', 'quality': 'Cardinal', 'symbol': '♈', 'lord': 'mars'},
    'taurus': {'element': 'Earth', 'quality': 'Fixed', 'symbol': '♉', 'lord': 'venus'},
    'gemini': {'element': 'Air', 'quality': 'Mutable', 'symbol': '♊', 'lord': 'mercury'},
    'cancer': {'element': 'Water', 'quality': 'Cardinal', 'symbol': '♋', 'lord': 'moon'},
    'leo': {'element': 'Fire', 'quality': 'Fixed', 'symbol': '♌', 'lord': 'sun'},
    'virgo': {'element': 'Earth', 'quality': 'Mutable', 'symbol': '♍', 'lord': 'mercury'},
    'libra': {'element': 'Air', 'quality': 'Cardinal', 'symbol': '♎', 'lord': 'venus'},
    'scorpio': {'element': 'Water', 'quality': 'Fixed', 'symbol': '♏', 'lord': 'mars'},
    'sagittarius': {'element': 'Fire', 'quality': 'Mutable', 'symbol': '♐', 'lord': 'jupiter'},
    'capricorn': {'element': 'Earth', 'quality': 'Cardinal', 'symbol': '♑', 'lord': 'saturn'},
    'aquarius': {'element': 'Air', 'quality': 'Fixed', 'symbol': '♒', 'lord': 'saturn'},
    'pisces': {'element': 'Water', 'quality': 'Mutable', 'symbol': '♓', 'lord': 'jupiter'},
}

PLANET_INFO = {
    'sun': {'symbol': '☉', 'represents': 'Soul, Authority, Career', 'element': 'Fire'},
    'moon': {'symbol': '☽', 'represents': 'Mind, Emotions, Mother', 'element': 'Water'},
    'mars': {'symbol': '♂', 'represents': 'Energy, Courage, Action', 'element': 'Fire'},
    'mercury': {'symbol': '☿', 'represents': 'Intellect, Communication', 'element': 'Earth'},
    'jupiter': {'symbol': '♃', 'represents': 'Wisdom, Prosperity, Growth', 'element': 'Ether'},
    'venus': {'symbol': '♀', 'represents': 'Love, Beauty, Relationships', 'element': 'Water'},
    'saturn': {'symbol': '♄', 'represents': 'Discipline, Karma, Patience', 'element': 'Air'},
    'rahu': {'symbol': '☊', 'represents': 'Ambition, Illusion, Foreign', 'element': 'Air'},
    'ketu': {'symbol': '☋', 'represents': 'Spirituality, Detachment', 'element': 'Fire'},
}


def calculate_julian_day(year, month, day, hour, minute, timezone_offset=5.5):
    """Calculate Julian Day Number for given date/time"""
    decimal_hour = hour + minute / 60.0 - timezone_offset
    return swe.julday(year, month, day, decimal_hour)


def get_rashi_from_degree(degree):
    """Get rashi name from degree (0-360)"""
    degree = degree % 360
    for rashi_name, rashi_full, start_deg, symbol in RASHIS:
        if start_deg <= degree < start_deg + 30:
            return rashi_name, degree - start_deg
    return 'aries', degree


def get_nakshatra_from_degree(degree):
    """Get nakshatra name, pada, and lord from degree (0-360)"""
    degree = degree % 360
    for i, (name, start, lord) in enumerate(NAKSHATRAS):
        end = NAKSHATRAS[(i + 1) % 27][1] if i < 26 else 360
        if start <= degree < end or (i == 26 and degree >= start):
            nakshatra_degree = degree - start
            pada = int(nakshatra_degree / 3.33) + 1
            return name, min(pada, 4), lord
    return NAKSHATRAS[0][0], 1, NAKSHATRAS[0][2]


def calculate_houses(julian_day, latitude, longitude):
    """Calculate house cusps using Placidus system"""
    houses = swe.houses_ex(julian_day, latitude, longitude, b'P')
    return houses[0]  # Array of 12 house cusps


def calculate_planet_positions(julian_day):
    """Calculate all planet positions"""
    positions = {}
    
    for planet_id, (name, full_name, symbol) in PLANETS.items():
        result = swe.calc_ut(julian_day, planet_id)
        degree = result[0][0]  # Longitude in degrees
        
        # Calculate Ayanamsa (Lahiri)
        ayanamsa = swe.get_ayanamsa_ut(julian_day)
        vedic_degree = (degree - ayanamsa) % 360
        
        rashi, degree_in_rashi = get_rashi_from_degree(vedic_degree)
        nakshatra, pada, nakshatra_lord = get_nakshatra_from_degree(vedic_degree)
        
        positions[name] = {
            'degree': round(vedic_degree, 2),
            'degree_in_rashi': round(degree_in_rashi, 2),
            'rashi': rashi,
            'nakshatra': nakshatra,
            'pada': pada,
            'symbol': symbol,
        }
    
    # Calculate Ketu
    if 'rahu' in positions:
        rahu_degree = positions['rahu']['degree']
        ketu_degree = get_ketu_position(rahu_degree)
        rashi, degree_in_rashi = get_rashi_from_degree(ketu_degree)
        nakshatra, pada, nakshatra_lord = get_nakshatra_from_degree(ketu_degree)
        
        positions['ketu'] = {
            'degree': round(ketu_degree, 2),
            'degree_in_rashi': round(degree_in_rashi, 2),
            'rashi': rashi,
            'nakshatra': nakshatra,
            'pada': pada,
            'symbol': '☋',
        }
    
    return positions


def assign_planets_to_houses(planet_positions, house_cusps):
    """Assign planets to houses based on house cusps"""
    ayanamsa = swe.get_ayanamsa_ut(swe.julday(1997, 2, 6, 17.5))
    
    # Convert house cusps to Vedic
    vedic_cusps = [(cusp - ayanamsa) % 360 for cusp in house_cusps]
    
    planet_houses = {}
    
    for planet_name, data in planet_positions.items():
        planet_degree = data['degree']
        
        # Find which house the planet is in
        for house_num in range(12):
            cusp_start = vedic_cusps[house_num]
            cusp_end = vedic_cusps[(house_num + 1) % 12]
            
            if cusp_start <= cusp_end:
                # Normal case
                if cusp_start <= planet_degree < cusp_end:
                    planet_houses[planet_name] = house_num + 1
                    break
            else:
                # House crosses 0°
                if planet_degree >= cusp_start or planet_degree < cusp_end:
                    planet_houses[planet_name] = house_num + 1
                    break
    
    return planet_houses


def calculate_house_scores(planet_positions, planet_houses):
    """Calculate strength scores for each house"""
    scores = {}
    
    for house_num in range(1, 13):
        score = 15  # Base score
        
        for planet_name, house in planet_houses.items():
            if house == house_num:
                planet_degree = planet_positions[planet_name]['degree_in_rashi']
                
                # Planets in own sign or exalted get bonus
                rashi = planet_positions[planet_name]['rashi']
                planet_key = planet_name.lower()
                
                # Add base points for having a planet
                score += 5
                
                # Check for directional strength (dig bala)
                if planet_name in ['jupiter', 'mercury'] and house_num == 1:
                    score += 3
                elif planet_name == 'sun' and house_num == 10:
                    score += 3
                elif planet_name == 'moon' and house_num == 4:
                    score += 3
                elif planet_name == 'mars' and house_num == 10:
                    score += 3
                elif planet_name == 'saturn' and house_num == 7:
                    score += 3
                elif planet_name == 'venus' and house_num == 4:
                    score += 3
        
        scores[house_num] = min(score, 36)  # Cap at 36
    
    return scores


def calculate_birth_chart():
    """Calculate complete birth chart for Jayti"""
    jd = calculate_julian_day(
        JAYTI_BIRTH_DATA['year'],
        JAYTI_BIRTH_DATA['month'],
        JAYTI_BIRTH_DATA['day'],
        JAYTI_BIRTH_DATA['hour'],
        JAYTI_BIRTH_DATA['minute']
    )
    
    # Calculate positions
    planet_positions = calculate_planet_positions(jd)
    
    # Calculate houses
    house_cusps = calculate_houses(jd, JAYTI_BIRTH_DATA['latitude'], JAYTI_BIRTH_DATA['longitude'])
    
    # Assign planets to houses
    planet_houses = assign_planets_to_houses(planet_positions, house_cusps)
    
    # Update planet positions with house info
    for planet_name, house in planet_houses.items():
        if planet_name in planet_positions:
            planet_positions[planet_name]['house'] = house
    
    # Determine ascendant (1st house cusp)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    ascendant_degree = (house_cusps[0] - ayanamsa) % 360
    ascendant_rashi, _ = get_rashi_from_degree(ascendant_degree)
    
    # Calculate house scores
    house_scores = calculate_house_scores(planet_positions, planet_houses)
    
    # Build house details
    houses = {}
    for i in range(12):
        house_num = i + 1
        cusp_degree = (house_cusps[i] - ayanamsa) % 360
        rashi, _ = get_rashi_from_degree(cusp_degree)
        
        planets_in_house = [
            name for name, h in planet_houses.items() if h == house_num
        ]
        
        houses[house_num] = {
            'rashi': rashi,
            'lord': RASHI_INFO[rashi]['lord'],
            'planets': planets_in_house,
            'score': house_scores.get(house_num, 15),
        }
    
    return {
        'ascendant': ascendant_rashi,
        'houses': houses,
        'planets': planet_positions,
    }


@login_required
def astro_dashboard(request):
    """Astrology dashboard overview"""
    chart_data = calculate_birth_chart()
    
    context = {
        'birth_data': JAYTI_BIRTH_DATA,
        'ascendant': chart_data['ascendant'],
        'rashi_info': RASHI_INFO[chart_data['ascendant']],
    }
    return render(request, 'astro/astro_dashboard.html', context)


@login_required
def birth_chart(request):
    """Display birth chart with visual representation"""
    chart_data = calculate_birth_chart()
    
    # Prepare chart data for display
    chart_display = []
    for house_num in range(1, 13):
        data = chart_data['houses'][house_num]
        
        planets_in_house = []
        for planet_name in data['planets']:
            if planet_name in chart_data['planets']:
                pdata = chart_data['planets'][planet_name]
                planets_in_house.append({
                    'name': planet_name,
                    'info': PLANET_INFO.get(planet_name, {}),
                    'degree': pdata.get('degree_in_rashi', 0),
                    'nakshatra': pdata.get('nakshatra', ''),
                    'symbol': pdata.get('symbol', ''),
                })
        
        chart_display.append({
            'number': house_num,
            'rashi': data['rashi'],
            'rashi_info': RASHI_INFO.get(data['rashi'], {}),
            'lord': data['lord'],
            'planets': planets_in_house,
            'score': data['score'],
        })
    
    # Prepare planet data for visual chart
    planets_for_chart = []
    for planet_name, pdata in chart_data['planets'].items():
        planets_for_chart.append({
            'name': planet_name,
            'symbol': pdata.get('symbol', ''),
            'house': pdata.get('house', 1),
            'rashi': pdata.get('rashi', 'aries'),
            'degree': pdata.get('degree_in_rashi', 0),
            'nakshatra': pdata.get('nakshatra', ''),
        })
    
    context = {
        'chart': chart_display,
        'ascendant': chart_data['ascendant'],
        'birth_data': JAYTI_BIRTH_DATA,
        'planets': planets_for_chart,
        'rashi_info': RASHI_INFO,
    }
    return render(request, 'astro/birth_chart.html', context)


@login_required
def house_details(request):
    """Detailed house analysis"""
    chart_data = calculate_birth_chart()
    
    house_meanings = {
        1: 'Self, Personality, Physical Appearance, Overall Well-being',
        2: 'Wealth, Family, Speech, Food, Face',
        3: 'Siblings, Courage, Communication, Short Travels, Skills',
        4: 'Home, Mother, Happiness, Vehicles, Education',
        5: 'Children, Creativity, Education, Speculation, Past Merit',
        6: 'Health, Enemies, Service, Debts, Competition',
        7: 'Marriage, Partnerships, Business, Foreign Lands',
        8: 'Transformation, Inheritance, Mysteries, Longevity, Sudden Events',
        9: 'Fortune, Higher Learning, Spirituality, Father, Long Travels',
        10: 'Career, Status, Father, Authority, Public Image',
        11: 'Gains, Friends, Aspirations, Elder Siblings, Fulfillment',
        12: 'Expenses, Liberation, Foreign Lands, Losses, Spirituality',
    }
    
    houses_detail = []
    
    for house_num in range(1, 13):
        data = chart_data['houses'][house_num]
        
        planets_in_house = []
        for planet_name in data['planets']:
            if planet_name in chart_data['planets']:
                pdata = chart_data['planets'][planet_name]
                planets_in_house.append({
                    'name': planet_name,
                    'info': PLANET_INFO.get(planet_name, {}),
                    'degree': pdata.get('degree_in_rashi', 0),
                    'nakshatra': pdata.get('nakshatra', ''),
                    'pada': pdata.get('pada', 1),
                    'symbol': pdata.get('symbol', ''),
                })
        
        strength = 'Strong' if data['score'] >= 25 else 'Moderate' if data['score'] >= 18 else 'Gentle'
        
        houses_detail.append({
            'number': house_num,
            'meaning': house_meanings[house_num],
            'rashi': data['rashi'],
            'rashi_info': RASHI_INFO.get(data['rashi'], {}),
            'lord': data['lord'],
            'lord_info': PLANET_INFO.get(data['lord'], {}),
            'planets': planets_in_house,
            'score': data['score'],
            'strength': strength,
        })
    
    context = {
        'houses': houses_detail,
    }
    return render(request, 'astro/house_details.html', context)


@login_required
def predictions(request):
    """90-day forward predictions based on current transits"""
    today = datetime.now().date()
    
    # Calculate current chart
    chart_data = calculate_birth_chart()
    
    # Generate predictions based on current transits
    predictions_data = generate_predictions(today, chart_data)
    
    context = {
        'predictions': predictions_data,
        'today': today,
    }
    return render(request, 'astro/predictions.html', context)


def generate_predictions(today, chart_data):
    """Generate 90-day predictions based on planetary positions and transits"""
    predictions = []
    
    # Get current planetary positions
    jd_today = calculate_julian_day(today.year, today.month, today.day, 12, 0)
    current_positions = calculate_planet_positions(jd_today)
    
    # Get natal positions for comparison
    natal_positions = chart_data['planets']
    
    # Career prediction (10th house focus)
    career_score = 0
    career_factors = []
    
    # Check Jupiter's transit
    if 'jupiter' in current_positions and 'jupiter' in natal_positions:
        jupiter_current = current_positions['jupiter']['house']
        jupiter_natal = natal_positions['jupiter'].get('house', 1)
        
        if jupiter_current == 10 or jupiter_natal == 10:
            career_score += 20
            career_factors.append("Jupiter's favorable influence on career house")
    
    # Check Saturn's transit
    if 'saturn' in current_positions:
        saturn_house = current_positions['saturn']['house']
        if saturn_house == 10:
            career_score += 10
            career_factors.append("Saturn bringing discipline to career matters")
    
    career_intensity = 'favorable' if career_score >= 20 else 'neutral' if career_score >= 10 else 'challenging'
    
    predictions.append({
        'period': 'Next 30 Days',
        'focus': 'Career',
        'intensity': career_intensity,
        'description': generate_career_description(career_score, career_factors),
        'recommendation': generate_career_recommendation(career_intensity),
        'dates': f"{today.strftime('%d %b')} - {(today + timedelta(days=30)).strftime('%d %b')}",
    })
    
    # Relationship prediction (7th house focus)
    relationship_score = 0
    rel_factors = []
    
    if 'venus' in current_positions:
        venus_house = current_positions['venus']['house']
        if venus_house in [7, 5, 11]:
            relationship_score += 15
            rel_factors.append("Venus supporting relationship harmony")
    
    rel_intensity = 'favorable' if relationship_score >= 15 else 'neutral'
    
    predictions.append({
        'period': 'Days 30-60',
        'focus': 'Relationships',
        'intensity': rel_intensity,
        'description': generate_relationship_description(relationship_score),
        'recommendation': 'Practice active listening. Express appreciation for loved ones. Be patient with family matters.',
        'dates': f"{(today + timedelta(days=30)).strftime('%d %b')} - {(today + timedelta(days=60)).strftime('%d %b')}",
    })
    
    # Health prediction (1st and 6th house focus)
    health_score = 0
    
    if 'saturn' in current_positions:
        saturn_house = current_positions['saturn']['house']
        if saturn_house in [1, 6]:
            health_score -= 10
    
    if 'sun' in current_positions:
        sun_house = current_positions['sun']['house']
        if sun_house == 1:
            health_score += 10
    
    health_intensity = 'favorable' if health_score > 0 else 'challenging' if health_score < 0 else 'neutral'
    
    predictions.append({
        'period': 'Days 60-90',
        'focus': 'Health',
        'intensity': health_intensity,
        'description': generate_health_description(health_intensity),
        'recommendation': 'Establish consistent sleep and exercise routines. Prioritize mental health through meditation or journaling.',
        'dates': f"{(today + timedelta(days=60)).strftime('%d %b')} - {(today + timedelta(days=90)).strftime('%d %b')}",
    })
    
    return predictions


def generate_career_description(score, factors):
    """Generate career prediction description"""
    if score >= 20:
        return "Jupiter aspects your 10th house, bringing opportunities for professional growth. This is a favorable time for initiating new projects and seeking recognition." + (f" {factors[0]}" if factors else "")
    elif score >= 10:
        return "Steady progress in career matters. Focus on building foundations and demonstrating reliability."
    else:
        return "A period for introspection regarding career direction. Avoid major decisions and focus on skill development."


def generate_career_recommendation(intensity):
    """Generate career recommendation"""
    if intensity == 'favorable':
        return "Take initiative on career goals. Network actively and present your ideas with confidence."
    elif intensity == 'neutral':
        return "Maintain steady effort. Focus on completing existing projects before starting new ones."
    else:
        return "Focus on skill development and learning. Avoid major career changes during this period."


def generate_relationship_description(score):
    """Generate relationship prediction description"""
    if score >= 15:
        return "Venus transits bring focus on partnerships. A time for deepening existing connections and healing past misunderstandings."
    else:
        return "Stable period for relationships. Focus on communication and understanding."


def generate_health_description(intensity):
    """Generate health prediction description"""
    if intensity == 'challenging':
        return "Saturn influence suggests the need for discipline in health routines. Minor stress-related issues may arise."
    elif intensity == 'favorable':
        return "Positive energy supporting vitality and well-being. Good time to start health initiatives."
    else:
        return "Maintain regular health routines. Pay attention to balance between work and rest."


@login_required
def planet_detail(request, planet):
    """Detailed information about a planet"""
    chart_data = calculate_birth_chart()
    
    if planet not in chart_data['planets']:
        messages.error(request, 'Planet not found.')
        return redirect('birth_chart')
    
    pdata = chart_data['planets'][planet]
    house = pdata.get('house', 1)
    rashi = pdata.get('rashi', 'aries')
    
    # Generate interpretation based on house position
    house_interpretations = {
        1: "In the 1st house, this planet significantly influences your personality and physical appearance.",
        2: "In the 2nd house, this planet affects your wealth, speech, and family matters.",
        3: "In the 3rd house, this planet influences your courage, siblings, and communication skills.",
        4: "In the 4th house, this planet affects your home, happiness, and relationship with mother.",
        5: "In the 5th house, this planet influences your creativity, children, and speculative gains.",
        6: "In the 6th house, this planet affects your health, competition, and ability to overcome obstacles.",
        7: "In the 7th house, this planet significantly influences your partnerships and marriage.",
        8: "In the 8th house, this planet affects transformation, inheritance, and longevity.",
        9: "In the 9th house, this planet influences your fortune, higher learning, and spirituality.",
        10: "In the 10th house, this planet strongly influences your career and public status.",
        11: "In the 11th house, this planet affects your gains, aspirations, and elder siblings.",
        12: "In the 12th house, this planet influences expenses, foreign connections, and liberation.",
    }
    
    context = {
        'planet': planet,
        'info': PLANET_INFO.get(planet, {}),
        'data': pdata,
        'house': house,
        'rashi': rashi,
        'rashi_info': RASHI_INFO.get(rashi, {}),
        'interpretation': house_interpretations.get(house, ""),
    }
    return render(request, 'astro/planet_detail.html', context)

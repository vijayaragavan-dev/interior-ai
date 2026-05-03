def analyze_room_layout(features):
    suggestions = []
    
    if not features['empty_walls']:
        suggestions.append({
            'category': 'Layout Warning',
            'text': 'Room appears fully furnished - consider decluttering for better TV placement',
            'priority': 'high'
        })
    
    if features['has_windows'] and features['has_doors']:
        if 'left' in features['empty_walls'] or 'right' in features['empty_walls']:
            suggestions.append({
                'category': 'TV Placement',
                'text': 'Best TV location: empty wall away from windows to reduce glare',
                'priority': 'high'
            })
    
    if features['has_shelves']:
        suggestions.append({
            'category': 'Storage',
            'text': 'Shelves detected - avoid placing TV on same wall for better viewing',
            'priority': 'medium'
        })
        suggestions.append({
            'category': 'Storage',
            'text': 'Use shelves for decorative items and books - keeps floor space clear',
            'priority': 'low'
        })
    
    return suggestions


def get_tv_placement_suggestions(features, style, budget):
    suggestions = []
    
    empty_count = len(features['empty_walls'])
    
    if empty_count >= 2:
        suggestions.append({
            'category': 'TV Placement',
            'text': 'Place TV on the longest empty wall for optimal viewing distance',
            'priority': 'high'
        })
        suggestions.append({
            'category': 'TV Placement',
            'text': 'Mount TV at 42-48 inches from floor (eye level when seated)',
            'priority': 'medium'
        })
    else:
        suggestions.append({
            'category': 'TV Placement',
            'text': 'Limited wall space - consider a TV stand or moving existing furniture',
            'priority': 'high'
        })
    
    if features['empty_walls']:
        wall_pos = features['empty_walls'][0].capitalize()
        suggestions.append({
            'category': 'TV Placement',
            'text': f'Recommended: Place TV on {wall_pos} wall for clean wall space',
            'priority': 'low'
        })
    
    if style.lower() in ['luxury', 'modern']:
        suggestions.append({
            'category': 'TV Setup',
            'text': 'Consider wall-mounted TV with hidden cable management',
            'priority': 'medium'
        })
    
    if budget.lower() == 'low':
        suggestions.append({
            'category': 'TV Setup',
            'text': 'Budget option: Use a sturdy TV stand with storage compartments',
            'priority': 'medium'
        })
    elif budget.lower() == 'high':
        suggestions.append({
            'category': 'TV Setup',
            'text': 'Premium option: Install motorized TV lift or projector screen',
            'priority': 'low'
        })
    
    return suggestions


def get_lighting_suggestions(color, style, room_size):
    suggestions = []
    
    suggestions.append({
        'category': 'Lighting',
        'text': 'Use warm LED lights (2700-3000K) for cozy atmosphere',
        'priority': 'high'
    })
    
    if style.lower() == 'minimal':
        suggestions.append({
            'category': 'Lighting',
            'text': 'Install recessed ceiling lights for clean, unobtrusive look',
            'priority': 'medium'
        })
    elif style.lower() == 'luxury':
        suggestions.append({
            'category': 'Lighting',
            'text': 'Add statement chandelier or pendant lights as focal point',
            'priority': 'high'
        })
    elif style.lower() == 'industrial':
        suggestions.append({
            'category': 'Lighting',
            'text': 'Use exposed bulb pendant lights with metal shades',
            'priority': 'medium'
        })
    elif style.lower() == 'scandinavian':
        suggestions.append({
            'category': 'Lighting',
            'text': 'Add floor lamp with natural materials (wood, rattan)',
            'priority': 'medium'
        })
    
    if color in ['purple luxury', 'navy blue', 'charcoal']:
        suggestions.append({
            'category': 'Lighting',
            'text': 'Add accent lighting to brighten darker wall colors',
            'priority': 'medium'
        })
    
    if room_size == 'small':
        suggestions.append({
            'category': 'Lighting',
            'text': 'Use mirrors opposite windows to reflect natural light',
            'priority': 'low'
        })
    
    suggestions.append({
        'category': 'Lighting',
        'text': 'Install dimmer switches for adjustable ambient lighting',
        'priority': 'low'
    })
    
    return suggestions


def get_color_suggestions(color, style, budget):
    suggestions = []
    
    color_guidance = {
        'purple luxury': {
            'walls': 'Apply purple to one accent wall only - keep other walls neutral white or cream',
            'complement': 'Pair with gold or brass decorative accents'
        },
        'grey modern': {
            'walls': 'Use grey on largest wall - adds depth and space illusion',
            'complement': 'Add white ceiling trim for contrast'
        },
        'mint green': {
            'walls': 'Mint works well in well-lit rooms - enhances natural freshness',
            'complement': 'Add natural wood furniture and plants'
        },
        'navy blue': {
            'walls': 'Navy creates drama - use on focal wall with white elsewhere',
            'complement': 'Add brass or gold hardware for elegance'
        },
        'terracotta': {
            'walls': 'Warm earth tone - perfect for creating cozy atmosphere',
            'complement': 'Pair with cream, beige, or warm white'
        },
        'sage green': {
            'walls': 'Sage adds calm - works with both warm and cool tones',
            'complement': 'Add natural linen and wooden elements'
        },
        'mustard yellow': {
            'walls': 'Bold choice - use on one wall for focal point',
            'complement': 'Balance with neutral furniture and grey accents'
        },
        'blush pink': {
            'walls': 'Soft and romantic - excellent for creating warmth',
            'complement': 'Add white furniture and rose gold accents'
        },
        'teal': {
            'walls': 'Rich teal works as accent - keeps other walls light',
            'complement': 'Add warm wood and terracotta for contrast'
        },
        'charcoal': {
            'walls': 'Modern and sophisticated - use on largest wall',
            'complement': 'Ensure good lighting - charcoal absorbs light'
        }
    }
    
    if color.lower() in color_guidance:
        suggestions.append({
            'category': 'Color',
            'text': color_guidance[color.lower()]['walls'],
            'priority': 'high'
        })
        suggestions.append({
            'category': 'Color',
            'text': color_guidance[color.lower()]['complement'],
            'priority': 'medium'
        })
    
    if budget.lower() == 'low':
        suggestions.append({
            'category': 'Color',
            'text': 'Budget tip: Use removable wallpaper or wall decals instead of paint',
            'priority': 'high'
        })
    elif budget.lower() == 'high':
        suggestions.append({
            'category': 'Color',
            'text': 'Premium: Consider textured wall panels or custom wall art',
            'priority': 'medium'
        })
    
    return suggestions


def get_style_suggestions(style, budget):
    suggestions = []
    
    style_guidance = {
        'modern': [
            'Keep furniture minimal with clean lines',
            'Use neutral color palette with one accent color',
            'Add functional storage to reduce visual clutter'
        ],
        'luxury': [
            'Add metallic (gold/brass) accents in lamps, frames, handles',
            'Use premium materials: marble, velvet, crystal',
            'Add statement furniture pieces as focal points'
        ],
        'minimal': [
            'Declutter before decorating - less is more',
            'Stick to essential furniture only',
            'Use hidden storage solutions'
        ],
        'scandinavian': [
            'Use light wood furniture with simple design',
            'Add cozy textiles: cushions, throws, rugs',
            'Maximize natural light with minimal window treatments'
        ],
        'industrial': [
            'Mix raw materials: exposed brick, metal, concrete',
            'Add vintage or repurposed furniture pieces',
            'Use Edison bulbs and metal light fixtures'
        ]
    }
    
    if style.lower() in style_guidance:
        for tip in style_guidance[style.lower()]:
            suggestions.append({
                'category': 'Style',
                'text': tip,
                'priority': 'medium'
            })
    
    if style.lower() == 'minimal' and budget.lower() == 'high':
        suggestions.append({
            'category': 'Style',
            'text': 'High budget minimal: Invest in built-in storage and hidden solutions',
            'priority': 'medium'
        })
    
    return suggestions


def get_budget_suggestions(budget, style):
    suggestions = []
    
    if budget.lower() == 'low':
        suggestions.append({
            'category': 'Budget',
            'text': 'Shop at local markets for affordable decor items',
            'priority': 'medium'
        })
        suggestions.append({
            'category': 'Budget',
            'text': 'DIY: Frame cheap prints or fabric as wall art',
            'priority': 'low'
        })
        suggestions.append({
            'category': 'Budget',
            'text': 'Repurpose existing furniture with fresh cushions or throws',
            'priority': 'medium'
        })
        suggestions.append({
            'category': 'Budget',
            'text': 'Use plants to add life - locally available plants are affordable',
            'priority': 'low'
        })
    elif budget.lower() == 'medium':
        suggestions.append({
            'category': 'Budget',
            'text': 'Invest in quality basics: sofa, bed, dining table',
            'priority': 'high'
        })
        suggestions.append({
            'category': 'Budget',
            'text': 'Mix high and low: splurge on key pieces, save on accessories',
            'priority': 'medium'
        })
    elif budget.lower() == 'high':
        suggestions.append({
            'category': 'Budget',
            'text': 'Invest in a quality sofa - it anchors the room',
            'priority': 'high'
        })
        suggestions.append({
            'category': 'Budget',
            'text': 'Consider custom built-in storage units',
            'priority': 'medium'
        })
        suggestions.append({
            'category': 'Budget',
            'text': 'Hire interior designer for professional space planning',
            'priority': 'low'
        })
    
    return suggestions


def get_practical_suggestions():
    suggestions = []
    
    suggestions.append({
        'category': 'Practical',
        'text': 'Use moisture-resistant paints for humid Indian climate',
        'priority': 'high'
    })
    suggestions.append({
        'category': 'Practical',
        'text': 'Add ventilation near cooking area if open to kitchen',
        'priority': 'medium'
    })
    suggestions.append({
        'category': 'Practical',
        'text': 'Use curtains that block light but allow ventilation',
        'priority': 'medium'
    })
    suggestions.append({
        'category': 'Storage',
        'text': 'Add floating shelves for display without cluttering floor',
        'priority': 'medium'
    })
    suggestions.append({
        'category': 'Practical',
        'text': 'Ensure electrical points are convenient for new furniture layout',
        'priority': 'low'
    })
    
    return suggestions


def generate_suggestions(color, style, budget, features=None):
    if features is None:
        features = {
            'has_windows': True,
            'has_doors': True,
            'has_shelves': False,
            'empty_walls': ['left', 'right'],
            'room_dimensions': {'width': 1200, 'height': 800}
        }
    
    all_suggestions = []
    
    w = features['room_dimensions']['width']
    room_size = 'small' if w < 1000 else 'medium' if w < 1500 else 'large'
    
    all_suggestions.extend(analyze_room_layout(features))
    all_suggestions.extend(get_tv_placement_suggestions(features, style, budget))
    all_suggestions.extend(get_lighting_suggestions(color, style, room_size))
    all_suggestions.extend(get_color_suggestions(color, style, budget))
    all_suggestions.extend(get_style_suggestions(style, budget))
    all_suggestions.extend(get_budget_suggestions(budget, style))
    all_suggestions.extend(get_practical_suggestions())
    
    seen = set()
    unique_suggestions = []
    for s in all_suggestions:
        key = s['text']
        if key not in seen:
            seen.add(key)
            unique_suggestions.append(s)
    
    return unique_suggestions
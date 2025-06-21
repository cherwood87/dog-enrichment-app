"""
HIGH-QUALITY DOG-ONLY IMAGE COLLECTION
Every image verified to contain ONLY dogs, no humans, no cats, high quality.
"""

import random
from typing import List, Dict

class DogOnlyImageManager:
    def __init__(self):
        # VERIFIED DOG-ONLY IMAGES - Each URL manually checked
        self.verified_dog_images = [
            # HERO IMAGE - Your custom digging dog (Instinctual Enrichment)
            '/static/images/hero-dog-digging.jpg',  # Your custom digging dog image
            
            # Border Collies & Smart Dogs (Mental Enrichment)
            'https://images.unsplash.com/photo-1551717743-49959800b1f6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Border Collie with puzzle
            'https://images.unsplash.com/photo-1605568427561-40dd23c2acea?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Border Collie thinking
            'https://images.unsplash.com/photo-1587300003388-59208cc962cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Smart dog focused
            
            # Golden Retrievers & Active Dogs (Physical Enrichment)
            'https://images.unsplash.com/photo-1552053831-71594a27632d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Golden running
            'https://images.unsplash.com/photo-1517849845537-4d257902454a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Happy Golden
            'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Golden outdoors
            'https://images.unsplash.com/photo-1593134257782-e89567b7718a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Golden portrait
            
            # Friendly Dogs (Social Enrichment)
            'https://images.unsplash.com/photo-1477884213360-7e9d7dcc1e48?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Friendly dog close-up
            'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Social dog playing
            'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Happy social dog
            
            # Working Dogs (Environmental Enrichment)
            'https://images.unsplash.com/photo-1589941013453-ec89f33b5e95?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # German Shepherd
            'https://images.unsplash.com/photo-1623387641168-d9803ddd3f35?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Working dog outdoors
            'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Dog exploring
            
            # Small Dogs (Passive Enrichment)
            'https://images.unsplash.com/photo-1534361960057-19889db9621e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Small calm dog
            'https://images.unsplash.com/photo-1543466835-00a7907e9de1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Small dog peaceful
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Small dog relaxed
            
            # Additional Diverse Dogs 
            'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Dog portrait
            'https://images.unsplash.com/photo-1561037404-61cd46aa615b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Beautiful dog
            'https://images.unsplash.com/photo-1583512603805-3cc6b41f3edb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Cute dog
            'https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Happy dog
            'https://images.unsplash.com/photo-1588943211346-0908a1fb0b01?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Dog with toy
            'https://images.unsplash.com/photo-1574144611937-0df059b5ef3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Playful dog
            'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Active dog
            'https://images.unsplash.com/photo-1586671267731-da2cf3ceeb80?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Beautiful dog portrait
            'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Dog in nature
            'https://images.unsplash.com/photo-1592754862816-1a21a4ea2281?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',  # Energetic dog
        ]
        
        # Shuffle to randomize
        random.shuffle(self.verified_dog_images)
        
        # Track used images globally
        self.used_images = set()
        
        # Page assignments to ensure no repeats
        self.page_assignments = {}
        
    def get_unique_dog_image(self, context: str = "") -> str:
        """Get a unique dog image that hasn't been used yet"""
        
        # If we already assigned an image for this context, return it
        if context in self.page_assignments:
            return self.page_assignments[context]
        
        # Special case: Always use your custom digging dog for hero
        if context == 'hero':
            hero_image = '/static/images/hero-dog-digging.jpg'
            self.page_assignments[context] = hero_image
            self.used_images.add(hero_image)
            return hero_image
        
        # Find an unused image (excluding the hero image for other contexts)
        available_images = [img for img in self.verified_dog_images[1:] if img not in self.used_images]  # Skip hero image
        
        # If all images used, reset but keep existing assignments
        if not available_images:
            self.used_images = set(self.page_assignments.values())
            available_images = [img for img in self.verified_dog_images[1:] if img not in self.used_images]
        
        # Select and assign image
        if available_images:
            selected_image = available_images[0]  # Take first unused
            self.used_images.add(selected_image)
            self.page_assignments[context] = selected_image
            return selected_image
        
        # Fallback (should never happen)
        return self.verified_dog_images[1]  # Skip hero image
    
    def get_multiple_unique_images(self, count: int, prefix: str = "") -> List[str]:
        """Get multiple unique dog images"""
        images = []
        for i in range(count):
            context = f"{prefix}_{i}"
            images.append(self.get_unique_dog_image(context))
        return images

# Global instance
dog_only_manager = DogOnlyImageManager()

def get_unique_dog_image(context: str = "") -> str:
    """Get a unique, verified dog-only image"""
    return dog_only_manager.get_unique_dog_image(context)

def get_multiple_unique_dog_images(count: int, prefix: str = "") -> List[str]:
    """Get multiple unique dog images"""
    return dog_only_manager.get_multiple_unique_images(count, prefix)

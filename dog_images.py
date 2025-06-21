"""
Dynamic Dog Image Management System

Provides diverse, unique dog images throughout the website to prevent repetition.
Uses a curated collection of high-quality dog photos from Unsplash.
"""

import random
from typing import List, Dict

class DogImageManager:
    def __init__(self):
        # Curated collection of diverse dog images from Unsplash
        # Organized by category to ensure variety
        self.dog_images = {
            'golden_retrievers': [
                'https://images.unsplash.com/photo-1552053831-71594a27632d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1517849845537-4d257902454a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1593134257782-e89567b7718a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            ],
            'border_collies': [
                'https://images.unsplash.com/photo-1551717743-49959800b1f6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1605568427561-40dd23c2acea?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1587300003388-59208cc962cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            ],
            'german_shepherds': [
                'https://images.unsplash.com/photo-1589941013453-ec89f33b5e95?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1605568427561-40dd23c2acea?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1551717743-49959800b1f6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1623387641168-d9803ddd3f35?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            ],
            'small_dogs': [
                'https://images.unsplash.com/photo-1534361960057-19889db9621e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1543466835-00a7907e9de1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            ],
            'puppies': [
                'https://images.unsplash.com/photo-1587300003388-59208cc962cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1477884213360-7e9d7dcc1e48?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            ],
            'working_dogs': [
                'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1605568427561-40dd23c2acea?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1623387641168-d9803ddd3f35?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            ],
            'mixed_breeds': [
                'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1534361960057-19889db9621e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1587300003388-59208cc962cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            ]
        }
        
        # Track used images to prevent repeats
        self.used_images = set()
        
        # Predefined image assignments for specific pages/sections
        self.page_assignments = {
            'hero': None,
            'mental_enrichment': None,
            'physical_enrichment': None,
            'social_enrichment': None,
            'environmental_enrichment': None,
            'instinctual_enrichment': None,
            'passive_enrichment': None,
        }
        
        # Generate assignments when class is initialized
        self._assign_page_images()
    
    def _assign_page_images(self):
        """Pre-assign unique images to each page section"""
        # Get all unique images
        all_images = []
        for category_images in self.dog_images.values():
            all_images.extend(category_images)
        
        # Remove duplicates while preserving order
        unique_images = list(dict.fromkeys(all_images))
        
        # Shuffle for randomness
        random.shuffle(unique_images)
        
        # Assign to each page section
        assignments = list(self.page_assignments.keys())
        for i, section in enumerate(assignments):
            if i < len(unique_images):
                self.page_assignments[section] = unique_images[i]
                self.used_images.add(unique_images[i])
    
    def get_image_for_section(self, section_name: str) -> str:
        """Get the assigned image for a specific section"""
        return self.page_assignments.get(section_name, self.get_random_unused_image())
    
    def get_random_unused_image(self) -> str:
        """Get a random image that hasn't been used yet"""
        # Get all unique images
        all_images = []
        for category_images in self.dog_images.values():
            all_images.extend(category_images)
        
        # Remove duplicates
        unique_images = list(dict.fromkeys(all_images))
        
        # Filter out used images
        available_images = [img for img in unique_images if img not in self.used_images]
        
        # If all images used, reset the used set (but keep page assignments)
        if not available_images:
            page_assigned_images = set(self.page_assignments.values())
            self.used_images = page_assigned_images.copy()
            available_images = [img for img in unique_images if img not in self.used_images]
        
        # Select random image
        if available_images:
            selected_image = random.choice(available_images)
            self.used_images.add(selected_image)
            return selected_image
        
        # Fallback to first available image
        return unique_images[0] if unique_images else ""
    
    def get_images_by_category(self, category: str, count: int = 1) -> List[str]:
        """Get specific number of images from a category"""
        if category not in self.dog_images:
            return [self.get_random_unused_image() for _ in range(count)]
        
        category_images = self.dog_images[category].copy()
        random.shuffle(category_images)
        
        result = []
        for _ in range(count):
            for img in category_images:
                if img not in self.used_images:
                    result.append(img)
                    self.used_images.add(img)
                    break
            else:
                # If no unused images in category, get any unused image
                result.append(self.get_random_unused_image())
        
        return result
    
    def get_breed_appropriate_image(self, breed_info: str) -> str:
        """Get an image appropriate for the given breed information"""
        breed_lower = breed_info.lower()
        
        if any(word in breed_lower for word in ['small', 'chihuahua', 'yorkie', 'pug']):
            return self.get_images_by_category('small_dogs', 1)[0]
        elif any(word in breed_lower for word in ['puppy', 'young', 'months']):
            return self.get_images_by_category('puppies', 1)[0]
        elif any(word in breed_lower for word in ['golden', 'retriever', 'lab']):
            return self.get_images_by_category('golden_retrievers', 1)[0]
        elif any(word in breed_lower for word in ['border', 'collie', 'shepherd']):
            return self.get_images_by_category('border_collies', 1)[0]
        elif any(word in breed_lower for word in ['german', 'working', 'large']):
            return self.get_images_by_category('working_dogs', 1)[0]
        else:
            return self.get_images_by_category('mixed_breeds', 1)[0]
    
    def reset_used_images(self):
        """Reset the used images tracker (but keep page assignments)"""
        page_assigned = set(self.page_assignments.values())
        self.used_images = page_assigned.copy()

# Global instance to use throughout the app
dog_image_manager = DogImageManager()

def get_dog_image(context: str = "random", breed_info: str = "") -> str:
    """
    Main function to get dog images throughout the app
    
    Args:
        context: What the image is for ('hero', 'mental_enrichment', etc.)
        breed_info: Information about the dog breed for appropriate image selection
    
    Returns:
        URL of an appropriate, unique dog image
    """
    if context in dog_image_manager.page_assignments:
        return dog_image_manager.get_image_for_section(context)
    elif breed_info:
        return dog_image_manager.get_breed_appropriate_image(breed_info)
    else:
        return dog_image_manager.get_random_unused_image()

def get_multiple_dog_images(count: int, category: str = "mixed") -> List[str]:
    """Get multiple unique dog images"""
    return dog_image_manager.get_images_by_category(category, count)

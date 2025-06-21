#!/usr/bin/env python3
"""
Auto Library Builder - Build large library without prompts
"""

from enhanced_library import EnhancedActivityLibrary

def build_large_library():
    print("🚀 Building Large Activity Library (20 per category)")
    print("=" * 55)
    
    library = EnhancedActivityLibrary()
    library.populate_library(target_per_category=20)  # 120 total activities
    
    print(f"\n🎯 Complete! You now have 120+ professional activities.")

if __name__ == "__main__":
    build_large_library()

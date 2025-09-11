#!/usr/bin/env python3
"""
Script para limpiar procesos de automatización que puedan estar colgados.
Útil para ejecutar manualmente cuando hay problemas de memoria o procesos zombi.

Uso:
    python scripts/cleanup_processes.py
    python scripts/cleanup_processes.py --aggressive
"""

import sys
import os
import time
import argparse

# Add the parent directory to the path so we can import from the project
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conftest import cleanup_browser_processes, force_cleanup_all_automation_processes
from logger import get_logger

def main():
    parser = argparse.ArgumentParser(description='Clean up automation processes')
    parser.add_argument('--aggressive', action='store_true', 
                       help='Use aggressive cleanup mode')
    parser.add_argument('--force', action='store_true',
                       help='Force cleanup all automation processes')
    
    args = parser.parse_args()
    
    # Initialize logger
    get_logger()
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info("Starting manual process cleanup...")
    
    if args.force:
        logger.info("Using force cleanup mode...")
        force_cleanup_all_automation_processes()
    else:
        logger.info(f"Using {'aggressive' if args.aggressive else 'normal'} cleanup mode...")
        cleanup_browser_processes(aggressive=args.aggressive)
    
    logger.info("Manual cleanup completed.")
    
    # Show memory usage
    try:
        import psutil
        memory = psutil.virtual_memory()
        logger.info(f"Current memory usage: {memory.percent}% ({memory.used / 1024**3:.1f} GB / {memory.total / 1024**3:.1f} GB)")
    except Exception as e:
        logger.warning(f"Could not get memory info: {e}")

if __name__ == "__main__":
    main()

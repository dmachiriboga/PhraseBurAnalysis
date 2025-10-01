#!/usr/bin/env python3
"""
BUR Histogram Visualization CLI
Creates histograms of BUR values for each performer.
"""

from visualization.bur_histograms import create_performer_bur_histograms

def main():
    output_dir = create_performer_bur_histograms()
    print(f"Histograms saved to {output_dir}/ (one PNG per performer)")

if __name__ == "__main__":
    main()
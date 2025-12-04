#!/usr/bin/env python3
"""
Filter private land parcels that are within the proposed fire district boundary.
"""
import json
import csv
from shapely.geometry import shape, Point, Polygon, MultiPolygon
from shapely.ops import unary_union

def load_geojson(filepath):
    """Load a GeoJSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def main():
    # Load the fire district boundary
    print("Loading proposed fire district boundary...")
    fire_district = load_geojson('proposed_fire_district.geojson')
    district_geometry = shape(fire_district['features'][0]['geometry'])

    # Load the private land parcels
    print("Loading private land parcels...")
    private_land = load_geojson('private_land_saguache.geojson')

    # Filter parcels within the district
    print(f"Processing {len(private_land['features'])} parcels...")
    filtered_parcels = []

    for i, feature in enumerate(private_land['features']):
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1} parcels...")

        parcel_geometry = shape(feature['geometry'])

        # Check if the parcel intersects with the fire district
        if district_geometry.intersects(parcel_geometry):
            # Calculate what percentage of the parcel is within the district
            intersection = district_geometry.intersection(parcel_geometry)
            overlap_ratio = intersection.area / parcel_geometry.area if parcel_geometry.area > 0 else 0

            # Add the properties along with overlap information
            parcel_data = feature['properties'].copy()
            parcel_data['overlap_ratio'] = overlap_ratio
            parcel_data['geometry_type'] = feature['geometry']['type']

            # Add centroid coordinates
            centroid = parcel_geometry.centroid
            parcel_data['centroid_lon'] = centroid.x
            parcel_data['centroid_lat'] = centroid.y

            filtered_parcels.append(parcel_data)

    print(f"\nFound {len(filtered_parcels)} parcels within the fire district.")

    # Write to CSV
    if filtered_parcels:
        output_file = 'private_land_in_fire_district.csv'
        print(f"Writing to {output_file}...")

        # Get all unique keys from all parcels
        all_keys = set()
        for parcel in filtered_parcels:
            all_keys.update(parcel.keys())

        fieldnames = sorted(all_keys)

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_parcels)

        print(f"Successfully wrote {len(filtered_parcels)} parcels to {output_file}")
    else:
        print("No parcels found within the fire district boundary.")

if __name__ == '__main__':
    main()

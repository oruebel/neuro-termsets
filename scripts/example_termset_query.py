import os
from pynwb import get_loaded_type_config
from pynwb.file import Subject
from hdmf.term_set import TermSet
import nwb_termsets

def main():
    # Load the termset configuration into PyNWB
    # This associates TermSets with specific PyNWB classes and fields 
    # (e.g., Subject.species, ElectrodeGroup.location)
    nwb_termsets.load_termset_config()

    # 1. Get the configured TermSet for Subject.species
    species_termset = nwb_termsets.get_configured_termsets(Subject, 'species')
    
    # 2. Look up and print the valid terms
    # The `view_set` property is a dictionary mapping term names (keys) to Term_Info objects
    print(f"\n--- Valid terms in the '{species_termset.name}' TermSet ---")
    for term_name, term_info in species_termset.view_set.items():
        print(f" - {term_name}: {term_info.description} (ID: {term_info.id})")

    # 3. Validate an example term against the TermSet
    species_term = "Mus musculus"
    is_valid = species_termset.validate(species_term)
    print(f"Is '{species_term}' valid? {is_valid}")
    
    # 4. Get the complete set of loaded termset configurations
    config = get_loaded_type_config()
    print("\n--- Loaded TermSet Configurations ---")
    for ns_name, ns_info in config.get('namespaces', {}).items():
        print(f"Namespace: {ns_name}")
        for dt_name, dt_info in ns_info.get('data_types', {}).items():
            print(f"  Data Type: {dt_name}")
            for attr_name, attr_info in dt_info.items():
                if 'termset' in attr_info:
                    print(f"    Attribute: {attr_name}, TermSet: {attr_info['termset']}")
       
if __name__ == "__main__":
    main()

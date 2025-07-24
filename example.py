#!/usr/bin/env python3
"""
Minimal example showing how Model converts biological hypotheses to sample_spec.
"""

import json
from typing import List, Dict, Any

def claude_hypothesis_to_sample_spec(hypothesis: str) -> List[Dict[str, Any]]:
    """
    Claude processes natural language hypothesis and generates sample_spec JSONs.
    In practice, this would call Claude API with biological reasoning prompts.
    """
    
    # Mock Claude's biological reasoning for: "p53 accumulation varies with cell density"
    if "p53" in hypothesis.lower() and "cell density" in hypothesis.lower():
        
        # Claude identifies key experimental parameters
        base_spec = {
            "schema_version": "1.0.0",
            "biological_context": {
                "cell_line": "HeLa",
                "passage_number": 12,
                "culture_age": 24
            },
            "culture_conditions": {
                "media_type": "DMEM",
                "media_supplements": ["10% FBS", "1% Pen/Strep"],
                "co2_percentage": 5,
                "temperature_celsius": 37
            },
            "treatments": {
                "compounds": [],
                "physical_perturbations": []
            },
            "sample_preparation": {
                "fixation_method": "paraformaldehyde",
                "fixation_duration": 15,
                "permeabilization": True,
                "blocking_agent": "5% goat_serum"
            },
            "staining_protocol": {
                "primary_antibodies": [{
                    "target": "p53",
                    "clone": "DO-1",
                    "concentration": 1,
                    "incubation_time": 60,
                    "temperature": 4
                }],
                "secondary_antibodies": [{
                    "fluorophore": "Alexa488",
                    "concentration": 2,
                    "incubation_time": 45
                }],
                "nuclear_stain": "DAPI"
            },
            "imaging_parameters": {
                "microscope_type": "confocal",
                "objective_magnification": 63,
                "channels": [
                    {"name": "DAPI", "excitation": 405, "emission": 450},
                    {"name": "Alexa488", "excitation": 488, "emission": 519}
                ]
            }
        }
        
        # Generate sample_specs for different cell densities
        densities = [25000, 50000, 75000, 100000]  # cells/cm²
        sample_specs = []
        
        for i, density in enumerate(densities):
            import copy
            spec = copy.deepcopy(base_spec)
            spec["sample_id"] = f"p53_density_exp_{i+1}"
            spec["biological_context"]["cell_density"] = density
            sample_specs.append(spec)
            
        return sample_specs
    
    else:
        raise NotImplementedError(f"Hypothesis not implemented: {hypothesis}")

def simulate_experimental_results(sample_specs: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Simulate experimental results for generated sample_specs.
    In practice, this data would come from laboratory automation systems.
    """
    results = {}
    
    for spec in sample_specs:
        sample_id = spec["sample_id"]
        density = spec["biological_context"]["cell_density"]
        
        # Simulate p53 intensity increasing with density (mock biological response)
        # Adding some noise to make it realistic
        import random
        base_intensity = density * 0.001  # Arbitrary scaling
        noise = random.uniform(-0.1, 0.1) * base_intensity
        p53_intensity = base_intensity + noise
        
        results[sample_id] = p53_intensity
        
    return results

def analyze_results(hypothesis: str, results: Dict[str, float]) -> Dict[str, Any]:
    """
    Analyze experimental results to validate/refute hypothesis.
    """
    sample_ids = sorted(results.keys())
    intensities = [results[sid] for sid in sample_ids]
    
    # Simple trend analysis
    increasing_trend = all(intensities[i] <= intensities[i+1] for i in range(len(intensities)-1))
    
    analysis = {
        "hypothesis": hypothesis,
        "results": results,
        "trend_increasing": increasing_trend,
        "conclusion": "Hypothesis supported" if increasing_trend else "Hypothesis not supported",
        "next_steps": []
    }
    
    if increasing_trend:
        analysis["next_steps"] = [
            "Test mechanism: contact inhibition vs nutrient depletion",
            "Validate with different cell lines",
            "Test temporal dynamics of p53 accumulation"
        ]
    else:
        analysis["next_steps"] = [
            "Re-examine experimental conditions",
            "Test alternative hypotheses"
        ]
    
    return analysis

def main():
    print("=== Model: Hypothesis Testing Example ===\n")
    
    # Step 1: Input biological hypothesis
    hypothesis = "p53 accumulation varies with cell density"
    print(f"Hypothesis: {hypothesis}\n")
    
    # Step 2: Claude converts hypothesis to sample_specs
    print("Generating sample_specs...")
    sample_specs = claude_hypothesis_to_sample_spec(hypothesis)
    print(f"Generated {len(sample_specs)} sample specifications:\n")
    
    for spec in sample_specs:
        density = spec["biological_context"]["cell_density"]
        print(f"  {spec['sample_id']}: {density} cells/cm²")
    
    # Step 3: Simulate experimental execution
    print("\nExecuting experiments...")
    results = simulate_experimental_results(sample_specs)
    
    print("Results:")
    for sample_id, intensity in results.items():
        print(f"  {sample_id}: p53 intensity = {intensity:.3f}")
    
    # Step 4: Analyze results
    print("\nAnalyzing results...")
    analysis = analyze_results(hypothesis, results)
    
    print(f"Conclusion: {analysis['conclusion']}")
    print("Next experimental steps:")
    for step in analysis['next_steps']:
        print(f"  - {step}")
    
    # Step 5: Show sample_spec for follow-up (if hypothesis supported)
    if analysis['trend_increasing']:
        print("\nGenerating follow-up experiment...")
        followup_hypothesis = "p53 accumulation is mediated by contact inhibition"
        print(f"Next hypothesis: {followup_hypothesis}")
        # In practice, this would generate new sample_specs for mechanism testing

if __name__ == "__main__":
    main()
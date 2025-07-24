# Sample Specification Schema

## Overview
The Sample_Spec defines the complete experimental context required to produce reproducible biological observations. This schema serves as both model input (describing conditions that produced experimental data) and model output (specifying conditions for the next experiment).

## Core Schema Structure

```json
{
  "sample_id": "string",
  "biological_context": {
    "cell_line": "string",
    "passage_number": "integer",
    "cell_density": "number",
    "culture_age": "number"
  },
  "culture_conditions": {
    "media_type": "string",
    "media_supplements": ["string"],
    "co2_percentage": "number",
    "temperature_celsius": "number",
    "humidity_percentage": "number",
    "atmospheric_oxygen": "number"
  },
  "treatments": {
    "compounds": [
      {
        "name": "string",
        "concentration": "number",
        "units": "string",
        "duration": "number",
        "time_units": "string"
      }
    ],
    "physical_perturbations": [
      {
        "type": "string",
        "parameters": "object"
      }
    ]
  },
  "sample_preparation": {
    "fixation_method": "string",
    "fixation_duration": "number",
    "permeabilization": "boolean",
    "blocking_agent": "string"
  },
  "staining_protocol": {
    "primary_antibodies": [
      {
        "target": "string",
        "clone": "string",
        "concentration": "number",
        "incubation_time": "number",
        "temperature": "number"
      }
    ],
    "secondary_antibodies": [
      {
        "fluorophore": "string",
        "concentration": "number",
        "incubation_time": "number"
      }
    ],
    "nuclear_stain": "string",
    "vital_dyes": ["string"]
  },
  "imaging_parameters": {
    "microscope_type": "string",
    "objective_magnification": "number",
    "numerical_aperture": "number",
    "channels": [
      {
        "name": "string",
        "excitation": "number",
        "emission": "number",
        "exposure_time": "number",
        "intensity": "number"
      }
    ],
    "z_stack": {
      "enabled": "boolean",
      "step_size": "number",
      "num_planes": "integer"
    },
    "time_lapse": {
      "enabled": "boolean",
      "interval": "number",
      "duration": "number"
    }
  },
  "assay_conditions": {
    "assay_type": "string",
    "reagents": [
      {
        "name": "string",
        "concentration": "number",
        "volume": "number"
      }
    ],
    "incubation_conditions": {
      "temperature": "number",
      "duration": "number",
      "shaking": "boolean"
    }
  },
  "metadata": {
    "experiment_date": "datetime",
    "operator": "string",
    "lab_conditions": {
      "ambient_temperature": "number",
      "ambient_humidity": "number"
    },
    "equipment_ids": ["string"],
    "notes": "string"
  }
}
```

## Field Categories

### 1. Biological Context
Core biological parameters that define the cellular system being studied.
- **cell_line**: Cell line identifier (e.g., "HeLa", "MCF-7", "primary_human_fibroblasts")
- **passage_number**: Number of times cells have been subcultured
- **cell_density**: Cells per unit area or volume at time of experiment
- **culture_age**: Time since initial plating or last passage

### 2. Culture Conditions  
Environmental parameters for cell growth and maintenance.
- **media_type**: Base culture medium (e.g., "DMEM", "RPMI-1640", "MEM")
- **media_supplements**: Additional components (e.g., ["10% FBS", "1% Pen/Strep"])
- **co2_percentage**: CO₂ concentration for pH buffering (typically 5%)
- **temperature_celsius**: Incubation temperature (typically 37°C)
- **humidity_percentage**: Relative humidity (typically 95%)
- **atmospheric_oxygen**: O₂ concentration (21% for normoxia, lower for hypoxia)

### 3. Treatments
Chemical compounds, physical perturbations, or other experimental interventions.
- **compounds**: Chemical treatments with concentration, duration, and timing
- **physical_perturbations**: Mechanical, electrical, or thermal interventions

### 4. Sample Preparation
Methods for preparing samples for analysis (fixation, permeabilization, etc.).
- **fixation_method**: Cell preservation method ("paraformaldehyde", "methanol", "live")
- **fixation_duration**: Time cells were fixed (if applicable)
- **permeabilization**: Whether cell membranes were permeabilized
- **blocking_agent**: Protein used to prevent non-specific binding

### 5. Staining Protocol
Fluorescent labeling and visualization methods.
- **primary_antibodies**: Target-specific antibodies with concentrations and conditions
- **secondary_antibodies**: Fluorophore-conjugated detection antibodies
- **nuclear_stain**: DNA-binding dyes (e.g., "DAPI", "Hoechst")
- **vital_dyes**: Live cell indicators (e.g., "calcein AM", "propidium iodide")

### 6. Imaging Parameters
Microscopy and data acquisition settings.
- **microscope_type**: Imaging system ("confocal", "widefield", "light_sheet")
- **objective_magnification**: Lens magnification (10x, 20x, 40x, 63x, 100x)
- **numerical_aperture**: Light-gathering capability of objective
- **channels**: Fluorescence channels with excitation/emission wavelengths
- **z_stack**: 3D imaging parameters
- **time_lapse**: Temporal imaging parameters

### 7. Assay Conditions
Biochemical assay parameters and conditions.
- **assay_type**: Type of biochemical measurement ("ELISA", "Western_blot", "qPCR")
- **reagents**: Assay-specific chemicals and their concentrations
- **incubation_conditions**: Temperature, time, and mixing parameters

### 8. Metadata
Experimental context and quality control information.
- **experiment_date**: When the experiment was performed
- **operator**: Person who conducted the experiment
- **lab_conditions**: Environmental conditions during experiment
- **equipment_ids**: Specific instruments used
- **notes**: Free-text observations or deviations from protocol

## Value Constraints and Validation Rules

### Required Fields
- `sample_id`: Must be unique identifier
- `biological_context.cell_line`: Must be non-empty string
- `experiment_date`: Must be valid datetime

### Numeric Constraints
- `passage_number`: Integer >= 0
- `cell_density`: Number > 0
- `temperature_celsius`: Number, typically 4-42°C range
- `co2_percentage`: Number, typically 0-10% range
- `humidity_percentage`: Number, 0-100% range
- `pH`: Number, typically 6.5-8.5 range
- `concentrations`: Numbers >= 0 with appropriate units

### Enumerated Values
- `fixation_method`: ["live", "paraformaldehyde", "methanol", "acetone", "glutaraldehyde"]
- `microscope_type`: ["widefield", "confocal", "two_photon", "light_sheet", "super_resolution"]
- `assay_type`: ["ELISA", "Western_blot", "qPCR", "flow_cytometry", "mass_spec", "luminescence"]
- `time_units`: ["seconds", "minutes", "hours", "days"]
- `concentration_units`: ["M", "mM", "µM", "nM", "mg/ml", "µg/ml", "ng/ml", "pg/ml"]

### Cross-Field Dependencies
- If `fixation_method` = "live", then `staining_protocol.vital_dyes` should be specified
- If `z_stack.enabled` = true, then `z_stack.step_size` and `z_stack.num_planes` are required
- If `time_lapse.enabled` = true, then `time_lapse.interval` and `time_lapse.duration` are required
- Treatment `duration` must be <= `culture_age`

### Format Specifications
- `sample_id`: Alphanumeric with underscores/hyphens, max 50 characters
- `experiment_date`: ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- `concentrations`: Scientific notation supported (e.g., "1e-6")
- `fluorophore`: Standard fluorophore names (e.g., "FITC", "PE", "APC", "Alexa488")

## Extensibility Mechanisms

### Custom Field Support
The schema supports extension through the `custom_fields` object in each major section:

```json
{
  "biological_context": {
    "cell_line": "HeLa",
    "passage_number": 15,
    "custom_fields": {
      "genetic_modifications": ["CRISPR_p53_knockout"],
      "selection_pressure": "G418_500ug_ml"
    }
  }
}
```

### Versioning
- Schema version field: `"schema_version": "1.0.0"`
- Backward compatibility maintained through version-aware parsing
- New fields added as optional to preserve compatibility

### Plugin Architecture
Support for domain-specific extensions:

```json
{
  "plugins": {
    "stem_cell_markers": {
      "pluripotency_factors": ["Oct4", "Sox2", "Nanog"],
      "differentiation_stage": "day_7_neural_induction"
    },
    "cancer_biology": {
      "tumor_grade": "grade_III",
      "metastatic_potential": "high"
    }
  }
}
```

### Dynamic Validation
- Validation rules can be extended via configuration files
- Custom validators for specialized equipment or protocols
- Context-dependent validation (e.g., cell-line-specific constraints)

### Equipment Integration
Extensible equipment specification:

```json
{
  "equipment_profiles": {
    "custom_microscope_xyz": {
      "manufacturer": "Custom Corp",
      "model": "XYZ-2000",
      "supported_channels": [405, 488, 561, 640],
      "max_magnification": 100,
      "special_capabilities": ["TIRF", "FRAP"]
    }
  }
}
```

## Documentation and Examples

### Example 1: Basic Live Cell Imaging
```json
{
  "sample_id": "exp_001_live_hela",
  "schema_version": "1.0.0",
  "biological_context": {
    "cell_line": "HeLa",
    "passage_number": 12,
    "cell_density": 50000,
    "culture_age": 24
  },
  "culture_conditions": {
    "media_type": "DMEM",
    "media_supplements": ["10% FBS", "1% Pen/Strep"],
    "co2_percentage": 5,
    "temperature_celsius": 37,
    "humidity_percentage": 95,
    "atmospheric_oxygen": 21
  },
  "treatments": {
    "compounds": [],
    "physical_perturbations": []
  },
  "sample_preparation": {
    "fixation_method": "live",
    "fixation_duration": null,
    "permeabilization": false,
    "blocking_agent": null
  },
  "staining_protocol": {
    "primary_antibodies": [],
    "secondary_antibodies": [],
    "nuclear_stain": "Hoechst",
    "vital_dyes": ["calcein_AM"]
  },
  "imaging_parameters": {
    "microscope_type": "widefield",
    "objective_magnification": 20,
    "numerical_aperture": 0.75,
    "channels": [
      {
        "name": "phase_contrast",
        "excitation": null,
        "emission": null,
        "exposure_time": 50,
        "intensity": 10
      },
      {
        "name": "DAPI",
        "excitation": 358,
        "emission": 461,
        "exposure_time": 100,
        "intensity": 25
      }
    ],
    "z_stack": {
      "enabled": false
    },
    "time_lapse": {
      "enabled": true,
      "interval": 300,
      "duration": 14400
    }
  }
}
```

### Example 2: Drug Treatment with Immunofluorescence
```json
{
  "sample_id": "exp_002_drug_treatment",
  "schema_version": "1.0.0",
  "biological_context": {
    "cell_line": "MCF-7",
    "passage_number": 8,
    "cell_density": 75000,
    "culture_age": 48
  },
  "treatments": {
    "compounds": [
      {
        "name": "doxorubicin",
        "concentration": 1,
        "units": "µM",
        "duration": 6,
        "time_units": "hours"
      }
    ]
  },
  "sample_preparation": {
    "fixation_method": "paraformaldehyde",
    "fixation_duration": 15,
    "permeabilization": true,
    "blocking_agent": "5% goat_serum"
  },
  "staining_protocol": {
    "primary_antibodies": [
      {
        "target": "p53",
        "clone": "DO-1",
        "concentration": 1,
        "incubation_time": 60,
        "temperature": 4
      }
    ],
    "secondary_antibodies": [
      {
        "fluorophore": "Alexa488",
        "concentration": 2,
        "incubation_time": 45
      }
    ],
    "nuclear_stain": "DAPI"
  },
  "imaging_parameters": {
    "microscope_type": "confocal",
    "objective_magnification": 63,
    "numerical_aperture": 1.4,
    "channels": [
      {
        "name": "DAPI",
        "excitation": 405,
        "emission": 450,
        "exposure_time": 200,
        "intensity": 2
      },
      {
        "name": "Alexa488",
        "excitation": 488,
        "emission": 519,
        "exposure_time": 500,
        "intensity": 5
      }
    ],
    "z_stack": {
      "enabled": true,
      "step_size": 0.2,
      "num_planes": 25
    }
  }
}
```

### Common Use Cases

#### 1. Live Cell Imaging Time Series
- Set `fixation_method: "live"`
- Enable `time_lapse` with appropriate intervals
- Use vital dyes for cell labeling
- Monitor cellular processes over time

#### 2. Drug Screening Experiments
- Define treatment compounds with concentrations
- Use fixed samples for endpoint analysis
- Include appropriate controls (vehicle, positive/negative)
- Optimize imaging for quantitative analysis

#### 3. Protein Localization Studies
- Use immunofluorescence staining protocols
- Enable z-stack imaging for 3D localization
- Include nuclear stain for cellular context
- Use high-resolution objectives (63x, 100x)

#### 4. Cell Cycle Analysis
- Combine DNA content staining with markers
- Use flow cytometry or imaging-based analysis
- Include cell cycle synchronization treatments
- Time points across cell cycle phases
# Used to rebuild entire Telomere STORM project analysis.
ML = matlab -nodesktop -r
ANALYSES_DIR = analyses
SAVED_DATA_DIR = saved_distrs

.PHONY: analyses
.PHONY: saveData
.PHONY: dataVis

# Runs all data processing steps
all: analyses saveData

# Process the localization data
analyses:
	$(MAKE) -C $(ANALYSES_DIR)

# Save processed Matlab data to text files
saveData: analyses
	$(MAKE) -C $(SAVED_DATA_DIR)

dataVis: analyses
	echo "Generating Matlab plots for process inspection."
	$(ML) "data_visualization_main()"

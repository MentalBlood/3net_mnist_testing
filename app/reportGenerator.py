import yaml

def generateReport(reportJSON):
	report = yaml.dump(reportJSON, default_flow_style=False, sort_keys=False)
	return report
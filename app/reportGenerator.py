import yaml

def generateReport(reportJSON):
	report = yaml.dump(reportJSON, default_flow_style=False, sort_keys=False)
	
	# for i in range(len(reportJSON)):
	# 	test = reportJSON[i]
	# 	report += 'TEST ' + i + ': ' + test['name'] + '\n'
	# 	for j in range(len(report['requests'])):
	# 		report += '\tREQUEST ' + j + ':' + '\n'
	# 		report += ''


	return report
# ============================================================================================================================
# PDF_Analyzer
# File   : main.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
# ============================================================================================================================


# TODO:

from osc_rule_based_extractor.globals import *
import argparse
from osc_rule_based_extractor.HTMLDirectory import *
from osc_rule_based_extractor.AnalyzerDirectory import *
from osc_rule_based_extractor.KPIResultSet import *
from osc_rule_based_extractor.TestData import *
from osc_rule_based_extractor.DataImportExport import *
from osc_rule_based_extractor.test import * #only for testing / debugging purpose
import osc_rule_based_extractor.config


from osc_rule_based_extractor import __version__

	
	
def load_kpis_from_directory(kpi_folder):
	kpis = []
	for filename in os.listdir(kpi_folder):
		if filename.endswith(".yaml") or filename.endswith(".yml"):
			filepath = os.path.join(kpi_folder, filename)
			print_verbose(2, "Loading KPI: " + str(filepath))
			k = KPISpecs.load_from_yaml(str(filepath))
			kpis.append(k)
	return kpis

	
	
def generate_dummy_test_data():

	test_data = TestData()
	test_data.generate_dummy_test_data(osc_rule_based_extractor.config.global_raw_pdf_folder, '*')
	#print("DATA-SET:")
	#print(test_data)		
	
	return test_data

def analyze_pdf(pdf_file, kpis, default_year, info_file_contents, wildcard_restrict_page='*', force_pdf_convert=False, force_parse_pdf=False, assume_conversion_done=False, do_wait=False):

	print_verbose(1, "Analyzing PDF: " +str(pdf_file))
	
	guess_year = Format_Analyzer.extract_year_from_text(pdf_file)
	if(guess_year is None):
		guess_year = default_year
	

	htmldir_path = get_html_out_dir(pdf_file)
	os.makedirs(htmldir_path, exist_ok=True)
	
	
	reload_neccessary = True
	

	if(not assume_conversion_done):
		#convert pdf to html
		print_big("Convert PDF to HTML", do_wait)
		if(force_pdf_convert or not file_exists(htmldir_path+'/index.html')):
			HTMLDirectory.convert_pdf_to_html(pdf_file, info_file_contents)


		#return KPIResultSet()# STOP after converting PDF files (dont continue with analysis)
			
		
		# parse and create json and png
		print_big("Convert HTML to JSON and PNG", do_wait)
		#print(htmldir_path)
		dir = HTMLDirectory()
		if(force_parse_pdf or get_num_of_files(htmldir_path+'/jpage*.json') != get_num_of_files(htmldir_path+'/page*.html') ): 
			dir.parse_html_directory(get_html_out_dir(pdf_file), 'page*.html') # ! page*
			dir.render_to_png(htmldir_path, htmldir_path)
			dir.save_to_dir(htmldir_path)
			#exit() #TODO: Remove this!!!!!
			if(wildcard_restrict_page == '*'):
				reload_neccessary = False
				
		#return KPIResultSet()# STOP after parsing HTML files (dont continue with analysis)

	# load json files
	print_big("Load from JSON", do_wait)
	if(reload_neccessary):
		dir = HTMLDirectory() 
		dir.load_from_dir(htmldir_path, 'jpage' + str(wildcard_restrict_page)  + '.json')
	

	# analyze 
	print_big("Analyze Pages", do_wait)
	ana = AnalyzerDirectory(dir, guess_year)
	#print(kpis)
	
	kpiresults = KPIResultSet(ana.find_multiple_kpis(kpis))
	
	
	print_big("FINAL RESULT FOR: "+ str(pdf_file.upper()), do_wait = False)
	print_verbose(1, kpiresults)	
	
	return kpiresults
	
	
	
def get_input_variable(val, desc):
	if val is None:
		val = input(desc)

	if(val is None or val==""):
		print("This must not be empty")
		sys.exit(0)
	
	return val
	
	
def main():

	DEFAULT_YEAR = 2019
	
	parser = argparse.ArgumentParser(description='Rule-based KPI extraction')
	# Add the arguments
	parser.add_argument('--pdftohtml_mod_executable',
						type=str,
						default=None,
						help='Path to executable pdftohtml_mod (can be found in git repository: osc-xpdf-mod)')
	parser.add_argument('--raw_pdf_folder',
						type=str,
						default=None,
						help='Folder where PDFs are stored')
	parser.add_argument('--working_folder',
						type=str,
						default=None,
						help='Folder where working files are stored')
	parser.add_argument('--kpi_folder',
						type=str,
						default=None,
						help='Folder where YAML files defining the KPIs are stored')
	parser.add_argument('--output_folder',
						type=str,
						default=None,
						help='Folder where output is stored')
	parser.add_argument('--verbosity',
						type=int,
						default=1,
						help='Verbosity level (0=shut up)')

	args = parser.parse_args()
	osc_rule_based_extractor.config.global_raw_pdf_folder = remove_trailing_slash(get_input_variable(args.raw_pdf_folder, "What is the raw pdf folder?")).replace('\\', '/') + r'/'
	osc_rule_based_extractor.config.global_working_folder = remove_trailing_slash(get_input_variable(args.working_folder, "What is the working folder?")).replace('\\', '/') + r'/'
	osc_rule_based_extractor.config.global_kpi_folder = remove_trailing_slash(get_input_variable(args.kpi_folder, "What is the path, where KPI YAML files are stored?")).replace('\\', '/') + r'/'
	osc_rule_based_extractor.config.global_output_folder =  remove_trailing_slash(get_input_variable(args.output_folder, "What is the output folder?")).replace('\\', '/') + r'/'
	osc_rule_based_extractor.config.global_verbosity = args.verbosity
	
	os.makedirs(osc_rule_based_extractor.config.global_working_folder, exist_ok=True)
	os.makedirs(osc_rule_based_extractor.config.global_output_folder, exist_ok=True)
	
	# fix osc_rule_based_extractor.config.global_exec_folder and osc_rule_based_extractor.config.global_rendering_font_override
	path = ''
	try:
		path = globals()['_dh'][0]
	except KeyError:
		path = os.path.dirname(os.path.realpath(__file__))
	path = remove_trailing_slash(path).replace('\\', '/')
	
	osc_rule_based_extractor.config.global_exec_folder = path+ r'/'
	osc_rule_based_extractor.config.global_rendering_font_override = path + r'/' + osc_rule_based_extractor.config.global_rendering_font_override
	osc_rule_based_extractor.config.global_approx_font_name = path + r'/' + osc_rule_based_extractor.config.global_approx_font_name
	osc_rule_based_extractor.config.global_pdftohtml_mod_executable = args.pdftohtml_mod_executable  #path + r'/' + osc_rule_based_extractor.config.global_pdftohtml_mod_executable
	
	print_verbose(1, "Using osc_rule_based_extractor.config.global_exec_folder=" + osc_rule_based_extractor.config.global_exec_folder)
	print_verbose(1, "Using osc_rule_based_extractor.config.global_raw_pdf_folder=" + osc_rule_based_extractor.config.global_raw_pdf_folder)
	print_verbose(1, "Using osc_rule_based_extractor.config.global_working_folder=" + osc_rule_based_extractor.config.global_working_folder)
	print_verbose(1, "Using osc_rule_based_extractor.config.global_kpi_folder=" + osc_rule_based_extractor.config.global_kpi_folder)
	print_verbose(1, "Using osc_rule_based_extractor.config.global_output_folder=" + osc_rule_based_extractor.config.global_output_folder)
	print_verbose(1, "Using osc_rule_based_extractor.config.global_verbosity=" + str(osc_rule_based_extractor.config.global_verbosity))
	print_verbose(1, "Using osc_rule_based_extractor.config.global_rendering_font_override=" + osc_rule_based_extractor.config.global_rendering_font_override)
	print_verbose(1, "Using osc_rule_based_extractor.config.global_approx_font_name=" + osc_rule_based_extractor.config.global_approx_font_name)
	print_verbose(1, "Using osc_rule_based_extractor.config.global_pdftohtml_mod_executable=" + osc_rule_based_extractor.config.global_pdftohtml_mod_executable)

	#test_data = load_test_data(r'test_data/aggregated_complete_samples_new.csv')
	test_data = generate_dummy_test_data()

	# For debugging, save csv:
	#test_data.save_to_csv(r'test_data/test_output_new.csv')
	#return
	
	
		
	
	# Filter PDF
	#test_data.filter_kpis(by_source_file = ['PGE_Corporation_CDP_Climate_Change_Questionnaire_2021.pdf']) 
	
		
	print_big("Data-set", False)
	print_verbose(1, test_data)


	pdfs = test_data.get_fixed_pdf_list()
	
	print_verbose(1, 'Related (fixed) PDFs: ' + str(pdfs) + ', in total : ' +str(len(pdfs)))
	#return ### TODO: Uncomment this line, to return immediately, after PDF list has been shown. ###
	


	kpis = load_kpis_from_directory(osc_rule_based_extractor.config.global_kpi_folder)
	
	overall_kpiresults = KPIResultSet()
	
	info_file_contents = DataImportExport.load_info_file_contents(remove_trailing_slash(osc_rule_based_extractor.config.global_working_folder) + '/info.json')
	
	time_start = time.time()
	
	for pdf in pdfs:
		kpiresults = KPIResultSet(kpimeasures = [])
		cur_kpiresults = analyze_pdf(osc_rule_based_extractor.config.global_raw_pdf_folder + pdf, kpis, DEFAULT_YEAR, info_file_contents, wildcard_restrict_page='*', assume_conversion_done=False, force_parse_pdf=False) ### TODO:  Modify * in order to analyze specfic page, e.g.:  *00042 ###
		kpiresults.extend(cur_kpiresults)
		overall_kpiresults.extend(cur_kpiresults)
		kpiresults.save_to_csv_file(osc_rule_based_extractor.config.global_output_folder + pdf + r'.csv')
		print_verbose(1, "RESULT FOR " + pdf)
		print_verbose(1, kpiresults)


		
	time_finish = time.time()
	
	print_big("FINAL OVERALL-RESULT", do_wait = False)
	print_verbose(1, overall_kpiresults)
	
	#overall_kpiresults.save_to_file(osc_rule_based_extractor.config.global_output_folder + r'kpiresults_test_tmp.json')
	#overall_kpiresults.save_to_csv_file(osc_rule_based_extractor.config.global_output_folder + r'kpiresults_tmp.csv')
	
	
	total_time = time_finish - time_start
	print_verbose(1, "Total run-time: " + str(total_time) + " sec ( " + str(total_time / max(len(pdfs), 1)) + " sec per PDF)")
	

	
	



if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m osc_rule_based_extractor.skeleton 42
    #
    main()

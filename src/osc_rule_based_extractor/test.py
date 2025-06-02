# ============================================================================================================================
# PDF_Analyzer
# File   : test.py
# Author : Ismail Demir (G124272)
# Date   : 05.08.2020
#
# Note: This file contains procedure used for testing only.
#
#
#
# ============================================================================================================================


from osc_rule_based_extractor.globals import *
from osc_rule_based_extractor.HTMLDirectory import *
from osc_rule_based_extractor.AnalyzerDirectory import *
from osc_rule_based_extractor.KPIResultSet import *
from osc_rule_based_extractor.TestData import *
from osc_rule_based_extractor.DataImportExport import *
from osc_rule_based_extractor.TestEvaluation import *
from osc_rule_based_extractor.test import * #only for testing / debugging purpose

def test(pdf_file, wildcard):
	
	dir = HTMLDirectory()
	dir.parse_html_directory(get_html_out_dir(pdf_file), r'page' + str(wildcard)  + '.html')
	dir.render_to_png(get_html_out_dir(pdf_file), get_html_out_dir(pdf_file))
	dir.save_to_dir(get_html_out_dir(pdf_file))


def test_convert_pdf(pdf_file):
	HTMLDirectory.convert_pdf_to_html(pdf_file)

	dir = HTMLDirectory()
	dir.parse_html_directory(get_html_out_dir(pdf_file), r'page*.html')
	dir.save_to_dir(get_html_out_dir(pdf_file))
	
	
def test_load_json(pdf_file, wildcard):
	
	dir = HTMLDirectory()
	dir.load_from_dir(get_html_out_dir(pdf_file), 'jpage' + str(wildcard)  + '.json')
	#dir.render_to_png(get_html_out_dir(pdf_file), get_html_out_dir(pdf_file))
	
	return dir
	
def test_save_json(dir):	
	dir.save_to_dir(get_html_out_dir(pdf_file))
	
	
def test_print_all_clusters(htmldir):
	for p in htmldir.htmlpages:
		print(p.clusters_text)



#
# Only used for initial testing
#		
def test_prepare_kpispecs():
	# TODO: This should be read from JSON files, but for now we can simply define it in code:
	
	
	
	
	def prepare_kpi_2_0_provable_plus_probable_reserves():
		# KPI 2.0 = proved plus probable reserves

		kpi = KPISpecs()
		kpi.kpi_id = 2.0
		kpi.kpi_name = 'Proven or probable reserves (Total hydrocarbons)'
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*prov.*develop.*undevelop.*reserv.*',score=12000,matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('proven develop or undevelop reserv')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*prov.*reserv.*',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 15, letter_decay_disregard = len('proven reserves')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*total.*hydrocarbon.*', score=15000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 15, letter_decay_disregard = len('total hydrocarbon')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(total|combine).*', score=2500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0.9, letter_decay_hl = 10, letter_decay_disregard = len('total')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*total.*(prov|prob).*reserv', score=5000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 15, letter_decay_disregard = len('total proven reserves')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*total.*reserv', score=4000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 15, letter_decay_disregard = len('total reserves')))
		
		#TODO: Check if we should add P50, like for KPI 2.1!
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*2p[\s]*reserv.*', score=4000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = len('2p reserves')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*prov.*probab.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = len('proved and proable')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'(.*(prov.*prob|prob.*prov).*|^((?!pro(b|v)).)*$)', score=1, matching_mode=MATCHING_MUST_INCLUDE_EACH_NODE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = True))

		
		
		kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(boe|barrel.*oil|(b|m)illion.*barrel).*',case_sensitive=False))
		kpi.value_must_be_numeric	= True
		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*exploration.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 2000, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = len('exploration')))
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*upstream.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 2000, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = len('upstream')))
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'^balance sheet.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 2000, matching_mode = MATCHING_MUST_EXCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = 0))

		#kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(prov|prob).*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 2000, matching_mode = MATCHING_MUST_INCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 8))
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*((^|[^a-z])prov|(^|[^a-z])2p($|[^a-z])).*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 500, matching_mode = MATCHING_MUST_INCLUDE, score_decay = 0.9, multi_match_decay=0.2, letter_decay_hl = 8, letter_decay_disregard = len('prov')))
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*((^|[^a-z])prob|(^|[^a-z])2p($|[^a-z])).*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 500, matching_mode = MATCHING_MUST_INCLUDE, score_decay = 0.9, multi_match_decay=0.2, letter_decay_hl = 8, letter_decay_disregard = len('prob')))
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*((^|[^a-z])pro(b|v).*(^|[^a-z])pro(b|v)|(^|[^a-z])2p($|[^a-z])).*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 2500, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.9, multi_match_decay=0.2, letter_decay_hl = 10, letter_decay_disregard = len('prov prob')))
		
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250
		
		return kpi


	def prepare_kpi_2_1_provable_reserves():
		# KPI 2.1 = proved reserves
		kpi = KPISpecs()
		kpi.kpi_id = 2.1
		kpi.kpi_name = 'Proven reserves (Total hydrocarbons)'
		
		#
		# TODO : Add kpi description here (similar to the procedure above!)
		#
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])prov.*develop.*undevelop.*reserv.*',score=12000,matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('proven develop or undevelop reserv')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])prov.*reserv.*',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 15, letter_decay_disregard = len('proven reserves')))

		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])prov.*reserv.*oil.*',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('proven reserves of oil and gas')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])prov.*reserv.*(oil.*gas|gas.*oil).*',score=15000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('proven reserves of oil and gas')))

		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*total.*hydrocarbon.*', score=1500, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 15, letter_decay_disregard = len('total hydrocarbon')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0.9, letter_decay_hl = 10, letter_decay_disregard = len('total')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*total.*prov.*reserv', score=5000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 15, letter_decay_disregard = len('total proven reserves')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*total.*reserv', score=4000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 15, letter_decay_disregard = len('total reserves')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*1p[\s]*(reserv|.*p90).*', score=4000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = len('1p reserves')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])prov.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = len('proved and proable')))

		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])sec.*',score=1000,matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 15, letter_decay_disregard = len('proven reserves sec')))
		
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'^((?!prob).)*$', score=1, matching_mode=MATCHING_MUST_INCLUDE_EACH_NODE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = True))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*prms.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = True))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*change.*(pro|reserv).*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))

		
		
		kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(boe|barrel.*oil|(b|m)illion.*barrel).*',case_sensitive=False))
		kpi.value_must_be_numeric	= True
		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*exploration.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 2000, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = len('exploration')))
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*upstream.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 2000, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = len('upstream')))
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'^balance sheet.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 2000, matching_mode = MATCHING_MUST_EXCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = 0))

		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*((^|[^a-z])prov|(^|[^a-z])1p($|[^a-z])).*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 500, matching_mode = MATCHING_MUST_INCLUDE, score_decay = 0.9, multi_match_decay=0.2, letter_decay_hl = 8, letter_decay_disregard = len('prov')))
		
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250		
		
		return kpi

		
		

	def prepare_kpi_3_production():
		# KPI 3 = production
		kpi = KPISpecs()
		kpi.kpi_id = 3
		kpi.kpi_name = 'Production'
		
		#
		# TODO : Add kpi description here (similar to the procedure above!)
		#
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*total.*production.*',score=5000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('total production')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*hydrocarbon.*production.*',score=5000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('hydrocarbon production')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*oil.*production.*',score=3000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('oil production')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*interest.*production.*',score=3000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('interest production')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*group.*',score=3000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('group production')))
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*apr.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*may.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*crease.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*change.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0.9, letter_decay_hl = 10, letter_decay_disregard = len('total')))
		
		
		kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(boe|barrel.*oil|(b|m)illion.*barrel|tonnes).*',case_sensitive=False))
		
		
		kpi.value_must_be_numeric	= True
		#kpi.value_percentage_match	= VALUE_PERCENTAGE_MUST_NOT
		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*production.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 100, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = len('production')))		
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250
		
		
		return kpi



	def prepare_kpi_3_1_oil_production():
		# KPI 3 = production
		kpi = KPISpecs()
		kpi.kpi_id = 3.1
		kpi.kpi_name = 'Oil Production'
		
		#
		# TODO : Add kpi description here (similar to the procedure above!)
		#
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*production.*',score=5000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('production')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*oil.*',score=5000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 1, letter_decay_hl = 20, letter_decay_disregard = len('oil production')))
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0.9, letter_decay_hl = 10, letter_decay_disregard = len('total')))
		
		
		kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(boe|barrel.*oil|(b|m)illion.*barrel|tonnes).*',case_sensitive=False))
		
		
		kpi.value_must_be_numeric	= True
		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*production.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 100, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = len('production')))		
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250
		
		
		return kpi



	def prepare_kpi_3_2_liquid_hydrocarbons_production():
		# KPI 3 = production
		kpi = KPISpecs()
		kpi.kpi_id = 3.2
		kpi.kpi_name = 'Liquid Hydrocarbons Production'
		
		#
		# TODO : Add kpi description here (similar to the procedure above!)
		#
		
		#kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*production.*',score=5000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('production')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*liquid.*hydrocarbon.*',score=5000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('liquid hydrocarbon')))
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0.9, letter_decay_hl = 10, letter_decay_disregard = len('total')))
		
		
		kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(boe|barrel.*oil|(b|m)illion.*barrel|ton|mt).*',case_sensitive=False))
		
		
		kpi.value_must_be_numeric	= True
		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*production.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 100, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = len('production')))		
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250
		
		
		return kpi



	def prepare_kpi_3_3_gas_production():
		# KPI 3 = production
		kpi = KPISpecs()
		kpi.kpi_id = 3.3
		kpi.kpi_name = 'Gas Production'
		
		#
		# TODO : Add kpi description here (similar to the procedure above!)
		#
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*production.*of.*gas.*',score=5000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('production gas')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*gas.*',score=3000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 1, letter_decay_hl = 20, letter_decay_disregard = len('gas')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*production.*',score=3000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('production')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*gas.*production.*',score=5000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl=20, letter_decay_disregard = len('gas production')))
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0.9, letter_decay_hl = 10, letter_decay_disregard = len('total')))
		
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*for.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*emission.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		
		
		kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(boe|barrel.*oil|(b|m)illion.*barrel|ton|mt|million|cm).*',case_sensitive=False))
		
		
		kpi.value_must_be_numeric	= True
		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*production.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 100, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = len('production')))		
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250
		
		
		return kpi		

	def prepare_Scope1_kpi_6_Direct_total_GHG_emissions():
		# KPI 6 = Scope 1 / Direct total GHGs emissions
		kpi = KPISpecs()
		kpi.kpi_id = 6
		kpi.kpi_name = 'Scope 1 / Direct total GHGs emissions'
		
		# Match paragraphs
		
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric|co2).*emissions?.*',score=7000 ,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('gas emissions')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])co2.*emissions?.*tCO2e.*',score=10000 ,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('co2 emissions')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*scope[^a-zA-Z0-9]?1.*',score=12000 ,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('scope 1')))



		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric|co2|combustion.*fuels?).*emissions?.*',score=7000 ,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('gas emissions')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])combustion.*fuels?.*',score=6000 ,matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('gas emissions')))

		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric).*(direct)(emissions?)?.*', score=9000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 15, letter_decay_disregard = len('gas direct')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric).*direct.*scope[^a-zA-Z0-9]?1(emissions?)?.*',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('direct scope 1')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])(greenhouse)?.*direct.*(gas|ghg|(ghg)|atmospheric).*scope[^a-zA-Z0-9]?1(emissions?)?.*',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('direct scope 1')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*scope\s1.*',score=6000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('proven reserves of oil and gas')))

		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric).*direct.*scope[^a-zA-Z0-9]?1(emissions?)?.*m.*t',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('proven reserves of oil and gas')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*scope[^a-zA-Z0-9]?2.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		#kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*group.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])(((gas|ghg|(ghg)|atmospheric)|direct).*emissions?|scope[^a-zA-Z0-9]?1).*(million\s? tonnes|co2[^a-zA-Z0-9]?eq)',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('proven reserves of oil and gas')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])((gas|ghg|(ghg)|atmospheric)|direct).*(million\s? tonnes|co2[^a-zA-Z0-9]?eq).*',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('proven reserves of oil and gas')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])direct.*(gas|ghg|(ghg)).*(million\s? tonnes|co2[^a-zA-Z0-9]?(eq|equivalent)).*',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('proven reserves of oil and gas')))

		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(scope[^a-zA-Z0-9]?2|scope[^a-zA-Z0-9]?3).*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*scope[^a-zA-Z0-9]?1,?[^a-zA-Z0-9]?2.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*scope[^a-zA-Z0-9]?1.*relative.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))

		
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])(greenhouse)?.*^(?=.*(gas|ghg|(ghg)|atmospheric))(?=.*direct)(?=.*scope[^a-zA-Z0-9]?1).*$(emissions?)?.*',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('proven reserves of oil and gas')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])(greenhouse)?.*^(?=.*(gas|ghg|(ghg)|atmospheric))(?=.*direct)(?=.*operated).*$(emissions?)?.*',score=6000,matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('proven reserves of oil and gas')))

		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])(greenhouse)?.*^(?=.*(gas|ghg|(ghg)|atmospheric))(?=.*direct).*$(emissions?)?.*',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('proven reserves of oil and gas')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])(greenhouse)?.*^(?=.*(gas|ghg|(ghg)|atmospheric))(?=.*scope[^a-zA-Z0-9]?1).*$(emissions?)?.*',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('proven reserves of oil and gas')))
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(^|[^a-z])direct.*emissions?.*',score=12000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 30, letter_decay_disregard = len('direct emissions')))

		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(total|combine).*', score=800, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 1, letter_decay_hl = 10, letter_decay_disregard = len('total indirect ghg  scope-2')))
		

		###     .*Direct NO.*emissions.*
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*direct no.*emissions.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(ton|mn|million|kt|m t|co 2|co.*emission).*',case_sensitive=False))

		#kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'.*((b|m)illions?.*(tons?|tonnes?).*CO2\s*equivalent|MteCO2e|mil\s*t\s*eq|(b|m)illions?\/teq|emissions.*CO2\s*equivalent).*',case_sensitive=False))
		kpi.value_must_be_numeric=True
		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(direct|ghg|gas).*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 500, matching_mode = MATCHING_CAN_INCLUDE, score_decay = 0.9, multi_match_decay=0.2, letter_decay_hl = 8, letter_decay_disregard = len('direct')))
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*scope[^a-zA-Z0-9]?1.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 500, matching_mode = MATCHING_CAN_INCLUDE, score_decay = 0.7, multi_match_decay=0.2, letter_decay_hl = 8, letter_decay_disregard = len('direct')))

		
		# added in particular for CDP reports:
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*gross global scope 1 emissions.*metric.*ton.*',score=20000 ,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('gross global scope 1 emissions metric ton')))
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*c6\.1.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 5000, matching_mode = MATCHING_CAN_INCLUDE, score_decay = 0.9, multi_match_decay=0.2, letter_decay_hl = 8, letter_decay_disregard = len('c6.1')))
		kpi.value_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'.*[0-9].*[0-9].*',case_sensitive=False)) # must contain at least two digits
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250

		
		return kpi
		
		




	def prepare_kpi_7_Scope2_GHGs_emissions():
		# KPI 7 = Scope 2 Energy indirect total GHGs emissions
		kpi = KPISpecs()
		kpi.kpi_id = 7
		kpi.kpi_name = 'Scope 2 Energy indirect total GHGs emissions'
		
		#
		# TODO : Add kpi description here (similar to the procedure above!)
		#
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*s.*cope( |-)2.*market',score=5000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('scope-2 market ')))

		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*s.*cope( |-)2.*',score=8000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('total indirect ghg  scope-2 ')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*indirect.*ghg.*',score=3000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 1, letter_decay_hl = 20, letter_decay_disregard = len('total indirect ghg  scope-2 ')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*ghg.*',score=3000,matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 1, letter_decay_hl = 20, letter_decay_disregard = len('total indirect ghg  scope-2 ')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*indirect.*',score=3000,matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 1, letter_decay_hl = 20, letter_decay_disregard = len('total indirect ghg  scope-2 ')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*co 2.*',score=3000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl=20, letter_decay_disregard = len('CO2')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*market.*',score=3000,matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 1, letter_decay_hl=20, letter_decay_disregard = len('total indirect ghg  scope 2  ')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*electricity.*',score=500,matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 1, letter_decay_hl=20, letter_decay_disregard = len('total indirect ghg  scope-2')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*indirect.*emissions.*',score=3000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 1, letter_decay_hl = 20, letter_decay_disregard = len('total indirect ghg  scope-2 ')))   #by Lei


		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 1, letter_decay_hl = 10, letter_decay_disregard = len('total indirect ghg  scope-2')))


		#kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(ton|mn|million|kt|m t|co 2).*', case_sensitive=False)) #by Lei
		
		
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*sale.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*s.*cope( |-)3.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(upstream|refin).*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))


		#eq does not work
		kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'^(t|.*(ton|mn|million|kt|m t|co 2).*)$',case_sensitive=False))
		
		
		kpi.value_must_be_numeric	= True
		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(environment|emission).*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 100, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = len('production')))		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*total.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 100, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = len('production')))		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*tons.*co.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 100, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.05, multi_match_decay=0.01, letter_decay_hl = 5, letter_decay_disregard = len('tons co2')))		#by Lei
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*million metric.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 200, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.05, multi_match_decay=0.01, letter_decay_hl = 5, letter_decay_disregard = len('million metric')))		#by Lei
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250
		
		
		return kpi



	def prepare_kpi_8_Scope3_GHGs_emissions():
		# KPI 8 = Scope 3 Upstream Energy indirect total GHGs emissions
		kpi = KPISpecs()
		kpi.kpi_id = 8
		kpi.kpi_name = 'Scope 3 Upstream Energy indirect total GHGs emissions'

		#
		# TODO : Add kpi description here (similar to the procedure above!)
		#

		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*s.*cope( |-)3.*',score=8000,matching_mode=MATCHING_MUST_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('total indirect ghg  scope-3 '))) #by Lei
#		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*s.*cope( |-)3.*',score=8000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('total indirect ghg  scope-3 ')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*ghg.*',score=3000,matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('total indirect ghg  scope-3 ')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*indirect.*',score=3000,matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('total indirect ghg  scope-3 ')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*emissions.*',score=3000,matching_mode=MATCHING_CAN_INCLUDE, score_decay=1, case_sensitive=False, multi_match_decay = 1, letter_decay_hl = 20, letter_decay_disregard = len('total indirect ghg  scope-3 ')))



		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('total indirect ghg  scope-3 ')))

		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*intensity.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*s.*cope( |-)2.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False)) #by Lei
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*305.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 10, letter_decay_disregard = 0, count_if_matched = False, allow_matching_against_concat_txt = False)) #by Lei



		kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(ton|mn|million|kt|m t|co 2).*',case_sensitive=False))
		
		
		kpi.value_must_be_numeric	= True
		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*(environment|emission).*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 100, matching_mode = MATCHING_MAY_INCLUDE, score_decay = 0.9, multi_match_decay=0.5, letter_decay_hl = 5, letter_decay_disregard = len('environment')))

		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250
		
		
		return kpi




	def prepare_kpi_12_Target_Year_Reduction():
		# KPI 12 = Target Year Reduction
		# this works right now only for CDP reports
		kpi = KPISpecs()
		kpi.kpi_id = 12
		kpi.kpi_name = 'Target Year Reduction'
		
		# Match paragraphs
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*targeted reduction from base year.*',score=8000 ,matching_mode=MATCHING_MUST_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('targeted reduction from base year')))
		
		kpi.value_must_be_numeric=True
		
		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*target year.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 5000, matching_mode = MATCHING_MUST_INCLUDE, score_decay = 0.9, multi_match_decay=0.2, letter_decay_hl = 8, letter_decay_disregard = len('c6.1')))
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*scope 1.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 5000, matching_mode = MATCHING_CAN_INCLUDE, score_decay = 0.9, multi_match_decay=0.2, letter_decay_hl = 8, letter_decay_disregard = len('c6.1')))
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*c4\.1a.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID, score = 5000, matching_mode = MATCHING_CAN_INCLUDE, score_decay = 0.9, multi_match_decay=0.2, letter_decay_hl = 8, letter_decay_disregard = len('c6.1')))
		
		kpi.value_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'[0-9]{2,3}(\.[0-9]+)?',case_sensitive=False)) # must be 2-3 digits, optional fractional part
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250

		
		return kpi


	def prepare_kpi_9991_CDP_0_4_Currency():
		# KPI 9991 = Currency of CDP Report
		# this works right now only for CDP reports
		kpi = KPISpecs()
		kpi.kpi_id = 9991
		kpi.kpi_name = 'C0.4 Currency of CDP Report'
		
		# Match paragraphs
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*\(c0\.4\) select the currency used.*',score=8000 ,matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('(C0.4) Select the currency used for all financial information disclosed throughout your')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*\(c0\.4\).*',score=2000 ,matching_mode=MATCHING_MUST_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('(C0.4) Select the currency used for all financial information disclosed throughout your')))
		
		kpi.value_must_be_numeric=False
		
		
		kpi.value_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'[A-Z]{3,3}',case_sensitive=True)) # must be 3 uppercase letters
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250

		
		return kpi
		
		
	def prepare_kpi_9992_CDP_4_1_Emiss_Target():
		# KPI 9992 = Emission Target CDP Report
		# this works right now only for CDP reports
		kpi = KPISpecs()
		kpi.kpi_id = 9991
		kpi.kpi_name = 'C4.1 Currency of CDP Report'
		
		# Match paragraphs
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*\(c4\.1\) *did you have an emissions target.*',score=8000 ,matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('(C4.1) Did you have an emissions target that was active in the reporting year?')))
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*\(c4\.1\).*',score=2000 ,matching_mode=MATCHING_MUST_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('(C4.1) Did you have an emissions target that was active in the reporting year?')))
		
		kpi.value_must_be_numeric=False
		
		
		kpi.value_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'[A-Z ]{3,35}target[A-Z ]{0,10}',case_sensitive=False)) # must be 3 uppercase letters
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250

		
		return kpi
		

		
		
	def prepare_kpi_9993_CDP_4_2b_Year_Target_Set():
		# KPI 9993 = CDP 4.b, year target set, for first target
		# this is more for testing/demonstration for CDP reports, dont use it productively yet
		kpi = KPISpecs()
		kpi.kpi_id = 9993
		kpi.kpi_name = 'C4.2b Year target set'
		
		# Match paragraphs
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*year target was set.*',score=8000 ,matching_mode=MATCHING_MUST_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('Year target was set')))
		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*\(c4\.2b\) *provide details of .*targets.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID_UP_ONLY, score = 5000, matching_mode = MATCHING_MUST_INCLUDE, score_decay = 0.9, multi_match_decay=0.2, letter_decay_hl = 8, letter_decay_disregard = len('(C4.2b) Provide details of any other climate-related targets, including methane')))
		
		kpi.value_must_be_numeric=True
		kpi.value_must_be_year = True
		
		
		kpi.value_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'(19[8-9]|20[0-2])[0-9]',case_sensitive=False)) # must be year 1980-2029
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250

		
		return kpi
		
		
		
	def prepare_kpi_9994_CDP_4_2b_Base_Year():
		# KPI 9993 = CDP 4.b, year target set, for first target
		# this is more for testing/demonstration for CDP reports, dont use it productively yet
		kpi = KPISpecs()
		kpi.kpi_id = 9994
		kpi.kpi_name = 'C4.2b Base year'
		
		# Match paragraphs
		kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw=r'.*base year.*',score=8000 ,matching_mode=MATCHING_MUST_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay = 0, letter_decay_hl = 20, letter_decay_disregard = len('Year target was set')))
		
		kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(general_match = KPISpecs.GeneralRegExMatch(pattern_raw=r'.*\(c4\.2b\) *provide details of .*targets.*',case_sensitive=False), distance_mode = DISTANCE_MOD_EUCLID_UP_ONLY, score = 5000, matching_mode = MATCHING_MUST_INCLUDE, score_decay = 0.9, multi_match_decay=0.2, letter_decay_hl = 8, letter_decay_disregard = len('(C4.2b) Provide details of any other climate-related targets, including methane')))
		
		kpi.value_must_be_numeric=True
		kpi.value_must_be_year = True
		
		
		kpi.value_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw=r'(19[8-9]|20[0-2])[0-9]',case_sensitive=False)) # must be year 1980-2029
		
		kpi.minimum_score = 500
		kpi.minimum_score_desc_regex = 250

		
		return kpi
		
		
		
	### TODO: Add new KPI definitions here ! (similar to the proceudres above: def prepare_...) ###	
		
		
		
		
		
		
	
	
		
	### TODO: Append relevant Kpi defintions to "res" : ###
	
	# Note: Tested for CDP:  kpi 6_1, 12, 9991

	res = []
	res.append(prepare_kpi_2_0_provable_plus_probable_reserves())
	res.append(prepare_kpi_2_1_provable_reserves())
	#res.append(prepare_kpi_2_2_probable_reserves()) #Not yet implemented! DO not comment in!!!
	res.append(prepare_kpi_3_production())
	res.append(prepare_kpi_3_1_oil_production())
	res.append(prepare_kpi_3_2_liquid_hydrocarbons_production())
	res.append(prepare_kpi_3_3_gas_production())
	res.append(prepare_Scope1_kpi_6_Direct_total_GHG_emissions())
	res.append(prepare_kpi_7_Scope2_GHGs_emissions())
	res.append(prepare_kpi_8_Scope3_GHGs_emissions())
	res.append(prepare_kpi_12_Target_Year_Reduction())
	res.append(prepare_kpi_9991_CDP_0_4_Currency())
	res.append(prepare_kpi_9992_CDP_4_1_Emiss_Target())
	res.append(prepare_kpi_9993_CDP_4_2b_Year_Target_Set())
	res.append(prepare_kpi_9994_CDP_4_2b_Base_Year())
	
	return res

	
	

def load_test_data(test_data_file_path):
	test_data = TestData()
	test_data.load_from_csv(test_data_file_path)
	
	# for testing purpose:
	#test_data.filter_kpis(by_kpi_id = [2], by_data_type = ['TABLE'])
	#test_data.filter_kpis(by_kpi_id = [2.1], by_data_type = ['TABLE'])
	#test_data.filter_kpis(by_kpi_id = [3], by_data_type = ['TABLE'])
	test_data.filter_kpis(by_kpi_id = [7], by_data_type = ['TABLE'])
	
	
	#print("DATA-SET:")
	#print(test_data)
	
	#print("PDF-Files:")
	#print(test_data.get_pdf_list())
	
	#fix_list = DataImportExport.import_files(r"/home/ismail/Share/initial_data/Europe", osc_rule_based_extractor.config.global_raw_pdf_folder, test_data.get_pdf_list(), 'pdf')
	fix_list = DataImportExport.import_files(r"//Wwg00m.rootdom.net/afs-team/1200000089/FC/R-M/AZUREPOC/2020/KPIs extraction/Training data/03_Oil Gas sector reports/Europe", osc_rule_based_extractor.config.global_raw_pdf_folder, test_data.get_pdf_list(), 'pdf')
	#fix_list = DataImportExport.import_files(r"//Wwg00m.rootdom.net/afs-team/1200000089/FC/R-M/AZUREPOC/2020/KPIs extraction/Training data", osc_rule_based_extractor.config.global_raw_pdf_folder, test_data.get_pdf_list(), 'pdf')
	test_data.fix_file_names(fix_list)
	
	
	# filter out entries with no source file:
	test_data.filter_kpis(by_has_fixed_source_file = True)
	
	#print("DATA-SET:")
	#print(test_data)	
	
	return test_data	
	
	

	
def test_analyze_directory(htmldirectoy):
	
	ana = AnalyzerDirectory(htmldirectoy, 2019)
	kpis = test_prepare_kpispecs()
	#print(kpis)
	
	kpiresults = KPIResultSet(ana.find_multiple_kpis(kpis))
	
	
	print_big("FINAL RESULT", do_wait = False)
	print(kpiresults)
	

	
	

def test_result():
	kpiresults = KPIResultSet()
	print(kpiresults)

	
	
	

def demo():

	pdf_file = osc_rule_based_extractor.config.global_raw_pdf_folder+r'test_bp.pdf'
	
	
	print_big("Convert PDF to HTML")
	HTMLDirectory.convert_pdf_to_html(pdf_file)

	
	print_big("Convert HTML to JSON and PNG")

	dir = HTMLDirectory()
	dir.parse_html_directory(get_html_out_dir(pdf_file), r'page*.html')
	dir.save_to_dir(get_html_out_dir(pdf_file))	
	dir.render_to_png(get_html_out_dir(pdf_file), get_html_out_dir(pdf_file))
	
	
	print_big("Load from JSON")
	dir = None
	dir = HTMLDirectory()
	dir.load_from_dir(get_html_out_dir(pdf_file) , r'jpage*.json')	
	
	print_big("Analyze Tables")
	test_analyze_directory(dir)


	
def test_main():
	PDF_FILE = osc_rule_based_extractor.config.global_raw_pdf_folder+r'04_NOVATEK_AR_2016_ENG_11.pdf'

	#test(PDF_FILE, "38")	
	
	dir = test_load_json(PDF_FILE, "*")
	
	test_analyze_directory(dir)
	
	
def test_evaluation():

	test_data = load_test_data(r'test_data/aggregated_complete_samples_new.csv')
	
	
	#test_data.filter_kpis(by_source_file = ['NYSE_TOT_2015 annual.pdf', 'LUKOIL_ANNUAL_REPORT_2018_ENG']) 
	
	
	test_data.filter_kpis(by_source_file = [                           
				'Aker-BP-Sustainability-Report-2019.pdf'                         # KPIs are on pg: 84: 2009:665.1 ... 2013:575.7
				#, 'NYSE_TOT_2018 annual.pdf'                       # KPIs are on pg: 129: 2017:914, 2018:917
				#, 'Transocean_Sustain_digital_FN_4 2017_2018.pdf'                        # KPIs are on pg: 112: 2016:711.1,  2015: 498.2
				#, 'Wintershall-Dea_Sustainability_Report_2019.pdf'
				])	
	
	print_big("Data-set", False)
	print(test_data)
	
	
	
	kpiresults = KPIResultSet.load_from_file(r'test_data/kpiresults_test_all_files_against_kpi_2_0.json')
	

	
	print_big("Kpi-Results", do_wait = False)
	print(kpiresults)
	
	
	print_big("Kpi-Evaluation", do_wait = False)
	
	kpis = test_prepare_kpispecs()
	
	test_eval = TestEvaluation.generate_evaluation(kpis, kpiresults, test_data)
	
	print(test_eval)
	
	
		
	
	

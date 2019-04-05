

# 'filing_number' and 'line_sequence' are added to all. 
## contributor_name for v <6
## payee_name 

SCHEDULE_A_HEADERS = ['filing_number', 'line_sequence', 'form_type', 'filer_committee_id_number', 'transaction_id', 'back_reference_tran_id_number', 'back_reference_sched_name', 'entity_type', 'contributor_organization_name', 'contributor_name', 'contributor_last_name', 'contributor_first_name', 'contributor_middle_name', 'contributor_prefix', 'contributor_suffix', 'contributor_street_1', 'contributor_street_2', 'contributor_city', 'contributor_state', 'contributor_zip_code', 'election_code', 'election_other_description', 'contribution_date', 'contribution_amount', 'contribution_aggregate', 'contribution_purpose_descrip', 'contributor_employer', 'contributor_occupation', 'donor_committee_fec_id', 'donor_committee_name', 'donor_candidate_fec_id', 'donor_candidate_last_name', 'donor_candidate_first_name', 'donor_candidate_middle_name', 'donor_candidate_prefix', 'donor_candidate_suffix', 'donor_candidate_office', 'donor_candidate_state', 'donor_candidate_district', 'conduit_name', 'conduit_street1', 'conduit_street2', 'conduit_city', 'conduit_state', 'conduit_zip_code', 'memo_code', 'memo_text_description', 'reference_code']

SCHEDULE_B_HEADERS = ['filing_number', 'line_sequence', 'form_type', 'filer_committee_id_number', 'transaction_id_number', 'back_reference_tran_id_number', 'back_reference_sched_name', 'entity_type', 'payee_organization_name', 'payee_name', 'payee_last_name', 'payee_first_name', 'payee_middle_name', 'payee_prefix', 'payee_suffix', 'payee_street_1', 'payee_street_2', 'payee_city', 'payee_state', 'payee_zip_code', 'election_code', 'election_other_description', 'expenditure_date', 'expenditure_amount', 'semi_annual_refunded_bundled_amt', 'expenditure_purpose_descrip', 'category_code', 'beneficiary_committee_fec_id', 'beneficiary_committee_name', 'beneficiary_candidate_fec_id', 'beneficiary_candidate_last_name', 'beneficiary_candidate_first_name', 'beneficiary_candidate_middle_name', 'beneficiary_candidate_prefix', 'beneficiary_candidate_suffix', 'beneficiary_candidate_office', 'beneficiary_candidate_state', 'beneficiary_candidate_district', 'conduit_name', 'conduit_street_1', 'conduit_street_2', 'conduit_city', 'conduit_state', 'conduit_zip_code', 'memo_code', 'memo_text_description', 'reference_to_si_or_sl_system_code_that_identifies_the_account']

# only copy the ones that need it
SCHEDULE_132_TO_A_MAPPING = {
    'donation_date':'contribution_date',
    'donation_amount':'contribution_amount',
    'donation_aggregate_amount':'contribution_aggregate_amount'
}


def remap_132_to_a(dict):
    for remapped_key in SCHEDULE_132_TO_A_MAPPING.keys():
        try:
            dict[SCHEDULE_132_TO_A_MAPPING[remapped_key]] = dict[remapped_key]
        except KeyError:
            print("KeyError %s" % remapped_key)
    return dict